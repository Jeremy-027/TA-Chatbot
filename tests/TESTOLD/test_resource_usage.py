# tests/test_resource_usage.py
import unittest
import sys
import os
import time
import psutil
import gc
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
    from response_generator import ResponseGenerator
    from fashion_mapping import FashionMapping


class TestResourceUsage(unittest.TestCase):
    """Test suite for measuring memory and CPU usage of various components"""

    def setUp(self):
        """Set up the components for resource usage testing"""
        # Gather baseline memory usage before creating any components
        self.process = psutil.Process(os.getpid())
        self.baseline_memory = self.process.memory_info().rss / (1024 * 1024)  # MB

        # For model-based components that require setup, use a fixture
        # but mock the actual model loading
        with patch("transformers.AutoTokenizer.from_pretrained"):
            with patch(
                "transformers.AutoModelForSequenceClassification.from_pretrained"
            ):
                self.processor = IndoBERTFashionProcessor("./fine-tuned-model")
                # Replace the model with a mock for initial tests
                self.processor.model = MagicMock()

        self.response_generator = ResponseGenerator()
        self.fashion_mapping = FashionMapping()

        # Force garbage collection to stabilize memory usage
        gc.collect()

    def get_memory_usage(self):
        """Get current memory usage in MB"""
        return self.process.memory_info().rss / (1024 * 1024)

    def get_cpu_usage(self):
        """Get current CPU usage percentage"""
        return self.process.cpu_percent(interval=None)

    def measure_resource_usage(self, function, *args):
        """Measure memory and CPU usage for a function call"""
        # Force garbage collection
        gc.collect()

        # Reset CPU usage measurement
        self.process.cpu_percent(interval=None)

        # Measure memory before
        memory_before = self.get_memory_usage()

        # Start timing
        start_time = time.time()

        # Execute function
        result = function(*args)

        # End timing
        end_time = time.time()

        # Measure memory after
        memory_after = self.get_memory_usage()

        # Measure CPU usage
        cpu_usage = self.get_cpu_usage()

        # Calculate metrics
        memory_delta = memory_after - memory_before
        execution_time = (end_time - start_time) * 1000  # ms

        return {
            "result": result,
            "memory_before": memory_before,
            "memory_after": memory_after,
            "memory_delta": memory_delta,
            "cpu_usage": cpu_usage,
            "execution_time": execution_time,
        }

    def test_response_generator_memory_usage(self):
        """Test memory usage of the response generator"""
        print("\nTesting Response Generator Memory Usage")

        test_params = [
            {"gender": "pria", "skin_tone": "light", "occasion": "formal"},
            {"gender": "wanita", "skin_tone": "dark", "occasion": "casual"},
            {"gender": "pria", "skin_tone": "light", "occasion": "wedding"},
            {"gender": "wanita", "skin_tone": "dark", "occasion": "party"},
            {
                "gender": "pria",
                "skin_tone": "light",
                "occasion": "casual",
                "weather": "hot",
            },
        ]

        for i, params in enumerate(test_params):
            metrics = self.measure_resource_usage(
                self.response_generator.generate_response, params
            )

            print(f"\nTest Case {i+1}: {params}")
            print(f"  Memory Before: {metrics['memory_before']:.2f} MB")
            print(f"  Memory After: {metrics['memory_after']:.2f} MB")
            print(f"  Memory Delta: {metrics['memory_delta']:.2f} MB")
            print(f"  CPU Usage: {metrics['cpu_usage']:.2f}%")
            print(f"  Execution Time: {metrics['execution_time']:.2f} ms")

            # Add assertions to catch memory leaks or excessive usage
            self.assertLess(
                metrics["memory_delta"],
                5,
                f"Memory increase should be less than 5MB, got {metrics['memory_delta']:.2f}MB",
            )

    def test_fashion_mapping_memory_usage(self):
        """Test memory usage of the fashion mapping"""
        print("\nTesting Fashion Mapping Memory Usage")

        test_params = [
            {"gender": "pria", "skin_tone": "light", "occasion": "formal"},
            {
                "gender": "wanita",
                "skin_tone": "dark",
                "occasion": "casual",
                "weather": "hot",
            },
            {
                "gender": "pria",
                "skin_tone": "light",
                "occasion": "formal",
                "season": "winter",
            },
        ]

        for i, params in enumerate(test_params):
            # First get recommendation
            recommendation = self.fashion_mapping.get_recommendation(params)

            # Then measure resource usage of format_recommendation
            metrics = self.measure_resource_usage(
                self.fashion_mapping.format_recommendation, recommendation, params
            )

            print(f"\nTest Case {i+1}: {params}")
            print(f"  Memory Before: {metrics['memory_before']:.2f} MB")
            print(f"  Memory After: {metrics['memory_after']:.2f} MB")
            print(f"  Memory Delta: {metrics['memory_delta']:.2f} MB")
            print(f"  CPU Usage: {metrics['cpu_usage']:.2f}%")
            print(f"  Execution Time: {metrics['execution_time']:.2f} ms")

            # Add assertions to catch memory leaks or excessive usage
            self.assertLess(
                metrics["memory_delta"],
                1,
                f"Memory increase should be less than 1MB, got {metrics['memory_delta']:.2f}MB",
            )

    def test_parameter_extraction_memory_usage(self):
        """Test memory usage of parameter extraction"""
        print("\nTesting Parameter Extraction Memory Usage")

        test_cases = [
            ("formal_pria_light", "Saya butuh baju formal untuk interview kerja"),
            (
                "casual_wanita_dark",
                "Outfit santai untuk jalan-jalan buat cewek kulit sawo matang",
            ),
            ("wedding", "Baju untuk pernikahan"),
        ]

        for i, (intent_name, text) in enumerate(test_cases):
            metrics = self.measure_resource_usage(
                self.processor.extract_parameters_from_intent, intent_name, text
            )

            print(f"\nTest Case {i+1}: Intent={intent_name}, Text='{text}'")
            print(f"  Memory Before: {metrics['memory_before']:.2f} MB")
            print(f"  Memory After: {metrics['memory_after']:.2f} MB")
            print(f"  Memory Delta: {metrics['memory_delta']:.2f} MB")
            print(f"  CPU Usage: {metrics['cpu_usage']:.2f}%")
            print(f"  Execution Time: {metrics['execution_time']:.2f} ms")

            # Add assertions to catch memory leaks or excessive usage
            self.assertLess(
                metrics["memory_delta"],
                0.5,
                f"Memory increase should be less than 0.5MB, got {metrics['memory_delta']:.2f}MB",
            )

    def test_repeated_calls_memory_stability(self):
        """Test memory stability with repeated calls to ensure no memory leaks"""
        print("\nTesting Memory Stability with Repeated Calls")

        test_params = {"gender": "pria", "skin_tone": "light", "occasion": "formal"}
        num_iterations = 50

        memory_readings = []

        print("  Running repeated calls and measuring memory...")
        for i in range(num_iterations):
            # Run a complete cycle of operations
            self.response_generator.generate_response(test_params)

            # Measure memory after each 10 iterations
            if i % 10 == 0:
                memory_usage = self.get_memory_usage()
                memory_readings.append(memory_usage)
                print(f"  Iteration {i}: Memory Usage = {memory_usage:.2f} MB")

        # Check if memory is stable
        if len(memory_readings) >= 3:
            # Calculate the slope of memory usage
            first_half_avg = sum(memory_readings[: len(memory_readings) // 2]) / (
                len(memory_readings) // 2
            )
            second_half_avg = sum(memory_readings[len(memory_readings) // 2 :]) / (
                len(memory_readings) - len(memory_readings) // 2
            )
            memory_slope = second_half_avg - first_half_avg

            print(f"\n  Memory slope: {memory_slope:.2f} MB")
            print(f"  First half average: {first_half_avg:.2f} MB")
            print(f"  Second half average: {second_half_avg:.2f} MB")

            # Assert that memory growth is minimal
            self.assertLess(
                memory_slope,
                5,
                f"Memory should be stable, but it grew by {memory_slope:.2f}MB over {num_iterations} iterations",
            )


if __name__ == "__main__":
    unittest.main()
