# tests/test_throughput.py
import unittest
import sys
import os
import time
import statistics
import threading
import concurrent.futures
from unittest.mock import patch, MagicMock

# Add the src directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# Create necessary mocks for components with external dependencies
with patch.dict(
    "sys.modules",
    {
        "torch": MagicMock(),
        "transformers": MagicMock(),
        "azure.cognitiveservices.speech": MagicMock(),
        "dotenv": MagicMock(),
    },
):
    from language_model import IndoBERTFashionProcessor
    from chatbot_azure import AzureFashionChatbot
    from chatbot_interface import FashionChatbot
    from response_generator import ResponseGenerator


class TestThroughput(unittest.TestCase):
    """Test suite for measuring the throughput capacity of the chatbot"""

    def setUp(self):
        """Set up the components for throughput testing"""
        # For model-based components that require setup, use a fixture
        # but mock the actual model loading
        with patch("transformers.AutoTokenizer.from_pretrained"):
            with patch(
                "transformers.AutoModelForSequenceClassification.from_pretrained"
            ):
                self.processor = IndoBERTFashionProcessor("./fine-tuned-model")
                # Replace the model with a mock for throughput tests
                self.processor.model = MagicMock()
                outputs = MagicMock()
                outputs.logits = MagicMock()
                self.processor.model.return_value = outputs

        # Create a text-only chatbot interface for throughput testing
        with patch(
            "language_model.IndoBERTFashionProcessor", return_value=self.processor
        ):
            self.chatbot = FashionChatbot(model_path="./mock-model")

        # Define a standard set of test queries covering different scenarios
        self.test_queries = [
            "Rekomendasi pakaian formal untuk pria",
            "Outfit casual untuk wanita berkulit sawo matang",
            "Baju untuk ke pernikahan",
            "Pakaian untuk cuaca panas",
            "Baju yang cocok untuk musim dingin",
            "Pakaian formal untuk interview kerja pria",
            "Outfit untuk hangout cewek kulit cerah",
            "Baju untuk ke pesta",
            "Pakaian untuk cuaca hujan",
            "Rekomendasi untuk ke kantor",
        ]

    def test_single_thread_throughput(self):
        """Test throughput capacity in a single thread"""
        print("\nTesting Single-Thread Throughput")

        num_requests = 50
        start_time = time.time()

        for i in range(num_requests):
            query = self.test_queries[i % len(self.test_queries)]
            response = self.chatbot.process_query(query)

        end_time = time.time()
        total_time = end_time - start_time
        throughput = num_requests / total_time

        print(f"  Processed {num_requests} requests in {total_time:.2f} seconds")
        print(f"  Throughput: {throughput:.2f} requests/second")

        # Add an assertion for minimum throughput
        self.assertGreater(
            throughput,
            5,
            f"Single-thread throughput should be at least 5 req/s, got {throughput:.2f}",
        )

    def test_multi_thread_throughput(self):
        """Test throughput capacity with multiple threads"""
        print("\nTesting Multi-Thread Throughput")

        num_threads = 5
        num_requests_per_thread = 20
        total_requests = num_threads * num_requests_per_thread

        def process_batch(thread_id):
            latencies = []
            start_time = time.time()

            for i in range(num_requests_per_thread):
                query_idx = (thread_id * num_requests_per_thread + i) % len(
                    self.test_queries
                )
                query = self.test_queries[query_idx]

                request_start = time.time()
                response = self.chatbot.process_query(query)
                request_end = time.time()

                latency = (request_end - request_start) * 1000  # ms
                latencies.append(latency)

            thread_time = time.time() - start_time
            return {
                "thread_id": thread_id,
                "requests_processed": num_requests_per_thread,
                "total_time": thread_time,
                "throughput": num_requests_per_thread / thread_time,
                "latencies": latencies,
            }

        # Execute the threads
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_to_thread = {
                executor.submit(process_batch, thread_id): thread_id
                for thread_id in range(num_threads)
            }

            results = []
            for future in concurrent.futures.as_completed(future_to_thread):
                thread_id = future_to_thread[future]
                result = future.result()
                results.append(result)
                print(
                    f"  Thread {thread_id} processed {result['requests_processed']} requests "
                    f"in {result['total_time']:.2f} seconds (Throughput: {result['throughput']:.2f} req/s)"
                )

        # Analyze results
        thread_throughputs = [r["throughput"] for r in results]
        avg_throughput = sum(thread_throughputs) / len(thread_throughputs)

        all_latencies = []
        for r in results:
            all_latencies.extend(r["latencies"])

        avg_latency = statistics.mean(all_latencies)
        max_latency = max(all_latencies)
        p90_latency = sorted(all_latencies)[int(len(all_latencies) * 0.9)]

        print(f"\n  Overall Multi-Thread Performance:")
        print(f"  Processed {total_requests} total requests with {num_threads} threads")
        print(f"  Average thread throughput: {avg_throughput:.2f} req/s")
        print(
            f"  Estimated system throughput: {avg_throughput * num_threads:.2f} req/s"
        )
        print(f"  Average latency: {avg_latency:.2f} ms")
        print(f"  90th percentile latency: {p90_latency:.2f} ms")
        print(f"  Maximum latency: {max_latency:.2f} ms")

        # Assert minimum multi-threaded throughput
        self.assertGreater(
            avg_throughput * num_threads,
            10,
            f"Multi-thread throughput should be at least 10 req/s",
        )

    def test_load_stability(self):
        """Test if the system maintains performance under sustained load"""
        print("\nTesting Load Stability Under Sustained Usage")

        num_batches = 3
        requests_per_batch = 20

        latency_by_batch = []
        throughput_by_batch = []

        for batch in range(num_batches):
            print(f"\n  Running batch {batch + 1}/{num_batches}...")

            batch_start = time.time()
            batch_latencies = []

            for i in range(requests_per_batch):
                query = self.test_queries[i % len(self.test_queries)]

                request_start = time.time()
                response = self.chatbot.process_query(query)
                request_end = time.time()

                latency = (request_end - request_start) * 1000  # ms
                batch_latencies.append(latency)

            batch_time = time.time() - batch_start
            batch_throughput = requests_per_batch / batch_time

            avg_batch_latency = statistics.mean(batch_latencies)
            latency_by_batch.append(avg_batch_latency)
            throughput_by_batch.append(batch_throughput)

            print(
                f"  Batch {batch + 1} - Avg Latency: {avg_batch_latency:.2f} ms, "
                f"Throughput: {batch_throughput:.2f} req/s"
            )

        # Check if performance is stable across batches
        latency_increase = latency_by_batch[-1] - latency_by_batch[0]
        throughput_decrease = throughput_by_batch[0] - throughput_by_batch[-1]

        print(f"\n  Performance Stability:")
        print(f"  Latency change from first to last batch: {latency_increase:.2f} ms")
        print(
            f"  Throughput change from first to last batch: {throughput_decrease:.2f} req/s"
        )

        # Assert stability thresholds
        self.assertLess(
            latency_increase,
            15,
            f"Latency increase should be less than 15ms, got {latency_increase:.2f}ms",
        )
        self.assertLess(
            throughput_decrease,
            2,
            f"Throughput decrease should be less than 2 req/s, got {throughput_decrease:.2f}",
        )

    def test_concurrent_request_patterns(self):
        """Test system performance with different concurrent request patterns"""
        print("\nTesting Performance with Different Concurrent Request Patterns")

        # Define different request patterns
        patterns = {
            "Uniform": [(i % len(self.test_queries)) for i in range(30)],
            "Repeated Same": [0] * 30,  # Always the first query
            "Alternating": [0, 1] * 15,  # Alternate between first and second
            "Burst": [i // 5 for i in range(30)],  # Groups of the same query
        }

        pattern_results = {}

        for pattern_name, query_indices in patterns.items():
            print(f"\n  Testing pattern: {pattern_name}")

            num_threads = 5
            requests_per_thread = len(query_indices) // num_threads

            def process_pattern(thread_id):
                latencies = []
                start_idx = thread_id * requests_per_thread
                end_idx = start_idx + requests_per_thread

                thread_start = time.time()

                for i in range(start_idx, end_idx):
                    query = self.test_queries[query_indices[i]]

                    request_start = time.time()
                    response = self.chatbot.process_query(query)
                    request_end = time.time()

                    latency = (request_end - request_start) * 1000  # ms
                    latencies.append(latency)

                thread_time = time.time() - thread_start
                return {
                    "thread_id": thread_id,
                    "latencies": latencies,
                    "avg_latency": statistics.mean(latencies),
                    "throughput": len(latencies) / thread_time,
                }

            # Execute the pattern with multiple threads
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=num_threads
            ) as executor:
                futures = [
                    executor.submit(process_pattern, t) for t in range(num_threads)
                ]

                results = []
                for future in concurrent.futures.as_completed(futures):
                    results.append(future.result())

            # Aggregate results for this pattern
            all_latencies = []
            throughputs = []

            for result in results:
                all_latencies.extend(result["latencies"])
                throughputs.append(result["throughput"])

            avg_latency = statistics.mean(all_latencies)
            avg_throughput = sum(throughputs)

            pattern_results[pattern_name] = {
                "avg_latency": avg_latency,
                "max_latency": max(all_latencies),
                "p95_latency": sorted(all_latencies)[int(len(all_latencies) * 0.95)],
                "throughput": avg_throughput,
            }

            print(f"  Results for pattern '{pattern_name}':")
            print(f"    Average Latency: {avg_latency:.2f} ms")
            print(
                f"    Max Latency: {pattern_results[pattern_name]['max_latency']:.2f} ms"
            )
            print(
                f"    P95 Latency: {pattern_results[pattern_name]['p95_latency']:.2f} ms"
            )
            print(f"    Throughput: {avg_throughput:.2f} req/s")

        # Compare performance across patterns
        print("\n  Pattern Performance Comparison:")
        for pattern, metrics in pattern_results.items():
            print(
                f"    {pattern}: {metrics['avg_latency']:.2f} ms latency, "
                f"{metrics['throughput']:.2f} req/s throughput"
            )

        # Assert reasonable performance across all patterns
        for pattern, metrics in pattern_results.items():
            self.assertLess(
                metrics["avg_latency"],
                100,
                f"Average latency for pattern '{pattern}' should be < 100ms",
            )
            self.assertGreater(
                metrics["throughput"],
                5,
                f"Throughput for pattern '{pattern}' should be > 5 req/s",
            )


if __name__ == "__main__":
    unittest.main()
