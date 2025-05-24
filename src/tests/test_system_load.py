# src/tests/test_system_load.py
import os
import sys
import time
import json
import threading
import queue
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import psutil
import traceback

# Add the parent directory to the path so we can import from src
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import required modules
from language_model import IndoBERTFashionProcessor


def monitor_system_resources(stop_event, metrics, interval=0.5):
    """Monitor system resources and record metrics."""
    cpu_usage = []
    memory_usage = []
    timestamps = []

    while not stop_event.is_set():
        # Record CPU usage
        cpu_percent = psutil.cpu_percent(interval=None)
        cpu_usage.append(cpu_percent)

        # Record memory usage
        process = psutil.Process(os.getpid())
        memory_info = process.memory_info()
        memory_mb = memory_info.rss / (1024 * 1024)  # Convert to MB
        memory_usage.append(memory_mb)

        # Record timestamp
        timestamps.append(time.time())

        # Sleep for the specified interval
        time.sleep(interval)

    # Store metrics
    metrics["cpu_usage"] = cpu_usage
    metrics["memory_usage"] = memory_usage
    metrics["timestamps"] = timestamps


def process_query(processor, query, results_queue):
    """Process a single query and record metrics."""
    try:
        start_time = time.time()

        # Step 1: NLP Processing
        intent_id = processor.classify_intent(query)
        sentiment = processor.analyze_sentiment(query)

        # Step 2: Response Generation
        text_response, json_response = processor.generate_response(
            query, intent_id, sentiment
        )

        end_time = time.time()
        processing_time = end_time - start_time

        # Check success
        success = text_response is not None and len(text_response) > 0

        # Store result
        result = {
            "query": query,
            "processing_time": processing_time,
            "success": success,
            "start_time": start_time,
            "end_time": end_time,
        }

        results_queue.put(result)

    except Exception as e:
        print(f"Error processing query: {query}")
        print(f"Error: {str(e)}")
        traceback.print_exc()

        results_queue.put(
            {
                "query": query,
                "processing_time": 0,
                "success": False,
                "start_time": time.time(),
                "end_time": time.time(),
                "error": str(e),
            }
        )


def test_system_load(model_path="./fine-tuned-model", duration=60, users=5):
    """Test system performance under load."""
    try:
        # Create results directory
        results_dir = "test_results"
        os.makedirs(results_dir, exist_ok=True)

        # Initialize processor
        print(
            f"Initializing processor for load testing with {users} concurrent users..."
        )
        processor = IndoBERTFashionProcessor(model_path)

        # Create test queries
        queries = [
            "Baju formal untuk interview",
            "Outfit casual untuk jalan-jalan",
            "Pakaian untuk cuaca panas",
            "Baju untuk ke pesta",
            "Rekomendasi fashion untuk musim dingin",
            "Saya pria berkulit cerah, mau ke meeting kantor",
            "Outfit untuk wanita berkulit sawo matang ke acara casual",
            "Baju formal yang professional looking",
        ]

        # Start monitoring system resources
        metrics = {}
        stop_monitoring = threading.Event()
        monitor_thread = threading.Thread(
            target=monitor_system_resources, args=(stop_monitoring, metrics)
        )
        monitor_thread.start()

        # Create results queue
        results_queue = queue.Queue()

        # Start the load test
        print(
            f"Starting load test for {duration} seconds with {users} concurrent users..."
        )
        start_time = time.time()
        threads = []
        query_count = 0

        try:
            # Run for the specified duration
            while time.time() - start_time < duration:
                # Create threads for concurrent users
                active_threads = sum(1 for t in threads if t.is_alive())
                new_threads_needed = users - active_threads

                for _ in range(new_threads_needed):
                    # Select a query (round-robin)
                    query = queries[query_count % len(queries)]
                    query_count += 1

                    # Create and start thread
                    thread = threading.Thread(
                        target=process_query, args=(processor, query, results_queue)
                    )
                    thread.start()
                    threads.append(thread)

                # Wait a bit before checking again
                time.sleep(0.1)

        finally:
            # Wait for all threads to finish
            print("Waiting for all threads to finish...")
            for thread in threads:
                thread.join(timeout=10)

            # Stop monitoring
            stop_monitoring.set()
            monitor_thread.join()

        # Get all results
        results = []
        while not results_queue.empty():
            results.append(results_queue.get())

        # Create results DataFrame
        results_df = pd.DataFrame(results)

        # Calculate statistics
        num_queries = len(results)
        queries_per_second = num_queries / duration
        success_rate = results_df["success"].mean() * 100 if not results_df.empty else 0
        avg_processing_time = (
            results_df["processing_time"].mean() if not results_df.empty else 0
        )
        p95_processing_time = (
            np.percentile(results_df["processing_time"], 95)
            if not results_df.empty
            else 0
        )

        # Create visualizations
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # CPU and Memory Usage over time
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

        # Adjust timestamps to be relative to start
        relative_timestamps = [
            t - metrics["timestamps"][0] for t in metrics["timestamps"]
        ]

        # CPU Usage
        ax1.plot(relative_timestamps, metrics["cpu_usage"])
        ax1.set_title("CPU Usage During Load Test")
        ax1.set_ylabel("CPU Usage (%)")
        ax1.grid(True)

        # Memory Usage
        ax2.plot(relative_timestamps, metrics["memory_usage"])
        ax2.set_title("Memory Usage During Load Test")
        ax2.set_xlabel("Time (seconds)")
        ax2.set_ylabel("Memory Usage (MB)")
        ax2.grid(True)

        plt.tight_layout()
        cpu_mem_plot = os.path.join(results_dir, f"load_test_resources_{timestamp}.png")
        plt.savefig(cpu_mem_plot)
        plt.close()

        # Processing Time Distribution
        plt.figure(figsize=(10, 6))
        plt.hist(results_df["processing_time"], bins=20)
        plt.xlabel("Processing Time (seconds)")
        plt.ylabel("Frequency")
        plt.title("Query Processing Time Distribution")
        plt.grid(True)
        proc_time_plot = os.path.join(
            results_dir, f"load_test_proc_times_{timestamp}.png"
        )
        plt.savefig(proc_time_plot)
        plt.close()

        # Concurrent Queries Over Time
        if not results_df.empty:
            # Create timeline of query starts and ends
            timeline = []
            for _, row in results_df.iterrows():
                timeline.append((row["start_time"], 1))  # Query start
                timeline.append((row["end_time"], -1))  # Query end

            # Sort by timestamp
            timeline.sort(key=lambda x: x[0])

            # Calculate concurrent queries at each point
            timestamps = [item[0] for item in timeline]
            changes = [item[1] for item in timeline]
            concurrent = 0
            concurrent_values = []

            for change in changes:
                concurrent += change
                concurrent_values.append(concurrent)

            # Adjust timestamps to be relative to start
            relative_timestamps = [t - timestamps[0] for t in timestamps]

            # Plot concurrent queries
            plt.figure(figsize=(12, 6))
            plt.step(relative_timestamps, concurrent_values, where="post")
            plt.xlabel("Time (seconds)")
            plt.ylabel("Concurrent Queries")
            plt.title("Concurrent Queries Over Time")
            plt.grid(True)
            concurrent_plot = os.path.join(
                results_dir, f"load_test_concurrent_{timestamp}.png"
            )
            plt.savefig(concurrent_plot)
            plt.close()

        # Save detailed results
        results_file = os.path.join(results_dir, f"load_test_results_{timestamp}.csv")
        if not results_df.empty:
            results_df.to_csv(results_file, index=False)

        # Create summary
        summary = {
            "timestamp": timestamp,
            "test_duration": duration,
            "concurrent_users": users,
            "total_queries_processed": num_queries,
            "queries_per_second": queries_per_second,
            "success_rate": success_rate,
            "average_processing_time": avg_processing_time,
            "p95_processing_time": p95_processing_time,
            "max_cpu_usage": max(metrics["cpu_usage"]) if metrics["cpu_usage"] else 0,
            "avg_cpu_usage": (
                sum(metrics["cpu_usage"]) / len(metrics["cpu_usage"])
                if metrics["cpu_usage"]
                else 0
            ),
            "max_memory_usage_mb": (
                max(metrics["memory_usage"]) if metrics["memory_usage"] else 0
            ),
            "final_memory_usage_mb": (
                metrics["memory_usage"][-1] if metrics["memory_usage"] else 0
            ),
        }

        # Save summary
        summary_file = os.path.join(results_dir, f"load_test_summary_{timestamp}.json")
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        # Print summary
        print("\n" + "=" * 60)
        print(f"System Load Test Summary:")
        print("-" * 60)
        print(f"Test Duration: {duration} seconds")
        print(f"Concurrent Users: {users}")
        print(f"Total Queries Processed: {num_queries}")
        print(f"Throughput: {queries_per_second:.2f} queries/second")
        print(f"Success Rate: {success_rate:.2f}%")
        print(f"Average Processing Time: {avg_processing_time:.4f} seconds")
        print(f"95th Percentile Processing Time: {p95_processing_time:.4f} seconds")
        print(f"Maximum CPU Usage: {max(metrics['cpu_usage']):.2f}%")
        print(
            f"Average CPU Usage: {sum(metrics['cpu_usage']) / len(metrics['cpu_usage']):.2f}%"
        )
        print(f"Maximum Memory Usage: {max(metrics['memory_usage']):.2f} MB")
        print("=" * 60)
        print(f"Detailed results saved to: {results_file}")
        print(f"Summary saved to: {summary_file}")
        print(f"Resource usage plot saved to: {cpu_mem_plot}")
        print(f"Processing time plot saved to: {proc_time_plot}")
        if not results_df.empty:
            print(f"Concurrent queries plot saved to: {concurrent_plot}")

        return summary, results_df

    except Exception as e:
        print(f"Error in system load testing: {str(e)}")
        traceback.print_exc()
        return None, None


if __name__ == "__main__":
    # Test with 5 concurrent users for 60 seconds
    test_system_load(users=5, duration=60)
