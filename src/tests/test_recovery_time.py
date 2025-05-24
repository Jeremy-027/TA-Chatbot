# src/tests/test_recovery_time.py
import os
import sys
import time
import json
import psutil
import signal
import subprocess
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Add the parent directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import chatbot components
from chatbot_azure import AzureFashionChatbot
from language_model import IndoBERTFashionProcessor


def create_failure_condition(scenario, process=None):
    """
    Create a specific failure condition to test recovery.

    Args:
        scenario (str): The failure scenario to create
        process (subprocess.Popen, optional): Process to manipulate for some scenarios

    Returns:
        None
    """
    print(f"Creating failure condition: {scenario}")

    if scenario == "cold_start":
        # Nothing to do - we'll test startup from scratch
        pass

    elif scenario == "speech_service_down":
        # Simulate Azure Speech service being unavailable by modifying environment variables
        # This is a simulation - in reality, Azure service outages would be external
        os.environ["AZURE_SPEECH_KEY"] = "invalid_key_for_testing"

    elif scenario == "model_crash":
        # Force termination of the model process or clear model from memory
        if process:
            os.kill(process.pid, signal.SIGTERM)
            time.sleep(2)  # Give time for process to terminate

    elif scenario == "memory_pressure":
        # Create memory pressure by allocating large arrays
        # Note: This is for testing only - be careful with memory allocations
        print("Creating memory pressure...")
        memory_hogs = []
        try:
            # Try to consume about 80% of available memory
            available = psutil.virtual_memory().available
            target = int(available * 0.8)
            chunk_size = 100 * 1024 * 1024  # 100 MB chunks

            while sum(len(x) for x in memory_hogs) * 8 < target:
                try:
                    memory_hogs.append([0.0] * (chunk_size // 8))
                except MemoryError:
                    break

            print(
                f"Allocated approximately {sum(len(x) for x in memory_hogs) * 8 / (1024*1024):.1f} MB"
            )
            time.sleep(5)  # Hold memory pressure briefly
        finally:
            # Release memory
            memory_hogs.clear()

    elif scenario == "high_cpu_load":
        # Create CPU load by spawning worker processes
        print("Creating high CPU load...")
        # Number of worker processes = CPU count
        cpu_count = psutil.cpu_count()
        workers = []

        try:
            # Create CPU-intensive processes
            for _ in range(cpu_count):
                # Execute a CPU-intensive Python process
                worker = subprocess.Popen(
                    [
                        sys.executable,
                        "-c",
                        "import time; [x**2 for x in range(100000000)]",
                    ]
                )
                workers.append(worker)

            # Let CPU load build for a few seconds
            time.sleep(10)
        finally:
            # Terminate workers
            for worker in workers:
                try:
                    worker.terminate()
                except:
                    pass

    else:
        print(f"Unknown scenario: {scenario}")

    print(f"Failure condition created for {scenario}")


def wait_for_recovery(test_function, timeout=60):
    """
    Wait for the system to recover until timeout.

    Args:
        test_function: Function that returns True if system is operational
        timeout (int): Maximum time to wait in seconds

    Returns:
        tuple: (recovered (bool), recovery_time (float))
    """
    print(f"Waiting for recovery (timeout: {timeout}s)...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            if test_function():
                recovery_time = time.time() - start_time
                print(f"System recovered in {recovery_time:.2f} seconds")
                return True, recovery_time
        except Exception as e:
            # System still recovering, ignore errors
            pass

        # Wait before next check
        time.sleep(1)

    print(f"Recovery timeout after {timeout} seconds")
    return False, timeout


def test_speech_functionality():
    """Test if speech service is functioning."""
    try:
        # Create a fresh chatbot instance
        chatbot = AzureFashionChatbot()

        # Test text-to-speech (this should work if Azure is available)
        chatbot.text_to_speech(
            "Test Message", is_error=True
        )  # Using is_error=True to avoid actual speech output
        return True
    except Exception as e:
        print(f"Speech test error: {str(e)}")
        return False


def test_nlp_functionality():
    """Test if NLP model is functioning."""
    try:
        # Create a new model instance
        processor = IndoBERTFashionProcessor("./fine-tuned-model")

        # Test intent classification
        intent = processor.classify_intent("Baju formal untuk interview")

        # If we got a valid intent, the model is working
        return intent is not None and isinstance(intent, int)
    except Exception as e:
        print(f"NLP test error: {str(e)}")
        return False


def test_end_to_end_functionality():
    """Test if the entire system is functioning end-to-end."""
    try:
        # Create a fresh chatbot instance
        chatbot = AzureFashionChatbot()

        # Process a test query
        response, is_error, _ = chatbot.process_input("Baju formal untuk interview")

        # Check if we got a valid response
        return not is_error and response is not None and len(response) > 0
    except Exception as e:
        print(f"End-to-end test error: {str(e)}")
        return False


def test_recovery_time():
    """Test system recovery from failures or restarts."""
    recovery_scenarios = [
        "cold_start",  # Starting from scratch
        "speech_service_down",  # Azure speech service unavailable
        "model_crash",  # NLP model crash
        "memory_pressure",  # System under memory pressure
        "high_cpu_load",  # System under high CPU load
    ]

    # Create results directory
    results_dir = "test_results"
    os.makedirs(results_dir, exist_ok=True)

    results = []
    for scenario in recovery_scenarios:
        print(f"\n{'='*50}")
        print(f"Testing recovery from {scenario}")
        print(f"{'='*50}")

        # For some scenarios, we need to start a process first
        process = None
        if scenario in ["model_crash"]:
            print("Starting process that will be crashed...")
            # Start a process that will be terminated
            process = subprocess.Popen(
                [
                    sys.executable,
                    "-c",
                    "import time; time.sleep(600)",
                ]  # Sleep for 10 minutes
            )

        # Create the failure condition
        create_failure_condition(scenario, process)

        # Determine which test function to use
        if scenario == "speech_service_down":
            test_function = test_speech_functionality
        elif scenario == "model_crash":
            test_function = test_nlp_functionality
        else:
            test_function = test_end_to_end_functionality

        # Measure recovery time
        recovered, recovery_time = wait_for_recovery(test_function, timeout=60)

        # Test system function after recovery
        post_recovery_function = False
        if recovered:
            print("Testing functionality after recovery...")
            post_recovery_function = test_end_to_end_functionality()

        # Record results
        results.append(
            {
                "scenario": scenario,
                "recovered": recovered,
                "recovery_time_seconds": recovery_time if recovered else None,
                "functional_after_recovery": post_recovery_function,
            }
        )

        # Clean up
        if scenario == "speech_service_down":
            # Restore environment variables
            if "AZURE_SPEECH_KEY" in os.environ:
                del os.environ["AZURE_SPEECH_KEY"]

        # Wait before next test
        time.sleep(5)

    # Create results DataFrame
    results_df = pd.DataFrame(results)

    # Calculate statistics
    success_rate = results_df["recovered"].mean() * 100
    functional_rate = results_df["functional_after_recovery"].mean() * 100
    avg_recovery_time = results_df[results_df["recovered"]][
        "recovery_time_seconds"
    ].mean()

    # Create visualizations
    plt.figure(figsize=(10, 6))
    for i, result in enumerate(results):
        if result["recovered"]:
            plt.bar(i, result["recovery_time_seconds"], color="green")
        else:
            plt.bar(i, 60, color="red")  # Use timeout value for failed recoveries

    plt.xticks(range(len(results)), [r["scenario"] for r in results], rotation=45)
    plt.ylabel("Recovery Time (seconds)")
    plt.title("System Recovery Time by Scenario")
    plt.tight_layout()

    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(results_dir, f"recovery_test_results_{timestamp}.csv")
    results_df.to_csv(results_file, index=False)

    plot_file = os.path.join(results_dir, f"recovery_test_plot_{timestamp}.png")
    plt.savefig(plot_file)
    plt.close()

    # Create summary
    summary = {
        "timestamp": timestamp,
        "scenarios_tested": len(results),
        "successful_recoveries": int(
            results_df["recovered"].sum()
        ),  # Convert numpy.int64 to int
        "recovery_success_rate": float(success_rate),  # Convert numpy.float64 to float
        "functional_after_recovery_rate": float(
            functional_rate
        ),  # Convert numpy.float64 to float
        "average_recovery_time": (
            float(avg_recovery_time) if not pd.isna(avg_recovery_time) else None
        ),  # Handle NaN
        "scenario_details": {},
    }

    # Manually build scenario details to ensure all values are JSON serializable
    for r in results:
        summary["scenario_details"][r["scenario"]] = {
            "recovered": bool(r["recovered"]),  # Convert to bool
            "recovery_time": (
                float(r["recovery_time_seconds"])
                if r["recovery_time_seconds"] is not None
                else None
            ),
            "functional_after": bool(r["functional_after_recovery"]),  # Convert to bool
        }

    # Save summary
    summary_file = os.path.join(results_dir, f"recovery_test_summary_{timestamp}.json")
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)

    # Print summary
    print("\n" + "=" * 60)
    print(f"Recovery Time Test Summary:")
    print("-" * 60)
    print(f"Scenarios Tested: {len(results)}")
    print(f"Successful Recoveries: {results_df['recovered'].sum()}/{len(results)}")
    print(f"Recovery Success Rate: {success_rate:.2f}%")
    print(f"Functional After Recovery: {functional_rate:.2f}%")
    print(f"Average Recovery Time: {avg_recovery_time:.2f} seconds")
    print("\nScenario Details:")
    for result in results:
        status = "✓" if result["recovered"] else "✗"
        time_str = (
            f"{result['recovery_time_seconds']:.2f}s"
            if result["recovered"]
            else "timeout"
        )
        functional = "✓" if result["functional_after_recovery"] else "✗"
        print(
            f"  {result['scenario']}: {status} Recovery: {time_str}, Functional: {functional}"
        )
    print("=" * 60)
    print(f"Detailed results saved to: {results_file}")
    print(f"Summary saved to: {summary_file}")
    print(f"Plot saved to: {plot_file}")

    return summary, results_df


if __name__ == "__main__":
    test_recovery_time()
