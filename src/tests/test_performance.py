# src/tests/test_performance.py
import unittest
import time
import threading
import queue
import statistics
from chatbot_azure import AzureFashionChatbot


class TestPerformance(unittest.TestCase):
    def setUp(self):
        self.test_queries = [
            "saya mencari pakaian formal untuk pria berkulit cerah",
            "rekomendasi pakaian casual untuk wanita berkulit sawo matang",
            "baju apa yang cocok untuk interview kerja?",
            # Add more queries
        ]

    def worker(self, worker_id, input_queue, results_queue):
        """Worker thread to process queries."""
        chatbot = AzureFashionChatbot()  # Each thread gets its own instance

        while not input_queue.empty():
            try:
                query = input_queue.get(timeout=1)
                start_time = time.time()
                response, is_error, _ = chatbot.process_input(query)
                end_time = time.time()

                results_queue.put(
                    {
                        "worker_id": worker_id,
                        "query": query,
                        "response_time": end_time - start_time,
                        "success": not is_error and response is not None,
                    }
                )

                input_queue.task_done()
            except queue.Empty:
                break

    def test_concurrent_processing(self):
        """Test system performance under concurrent load."""
        # Test with different numbers of concurrent users
        for num_concurrent in [1, 5, 10, 20]:
            print(f"\nTesting with {num_concurrent} concurrent users")

            # Create queues
            input_queue = queue.Queue()
            results_queue = queue.Queue()

            # Fill input queue with repeated queries to simulate load
            for _ in range(num_concurrent * 5):  # 5 queries per simulated user
                for query in self.test_queries:
                    input_queue.put(query)

            # Create and start worker threads
            threads = []
            for i in range(num_concurrent):
                thread = threading.Thread(
                    target=self.worker, args=(i, input_queue, results_queue)
                )
                threads.append(thread)
                thread.start()

            # Wait for all threads to finish
            for thread in threads:
                thread.join()

            # Analyze results
            results = []
            success_count = 0

            while not results_queue.empty():
                result = results_queue.get()
                results.append(result)
                if result["success"]:
                    success_count += 1

            response_times = [r["response_time"] for r in results]

            avg_response_time = statistics.mean(response_times)
            p95_response_time = statistics.quantiles(response_times, n=20)[
                18
            ]  # 95th percentile
            success_rate = success_count / len(results) if results else 0

            print(f"Success Rate: {success_rate:.4f}")
            print(f"Average Response Time: {avg_response_time:.4f} seconds")
            print(f"P95 Response Time: {p95_response_time:.4f} seconds")

            # For load testing, we're just collecting metrics, not asserting
