# tests/test_performance_latency.py
import unittest
import sys
import os
import time
import statistics
import json
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


class TestPerformanceLatency(unittest.TestCase):
    """Test suite for measuring the latency of various components"""

    def setUp(self):
        """Set up the components for latency testing"""
        # For most latency tests, we want to use real implementations
        # rather than mocks to measure actual performance
        self.response_generator = ResponseGenerator()
        self.fashion_mapping = FashionMapping()

        # For model-based components that require setup, use a fixture
        # but mock the actual model loading
        with patch("transformers.AutoTokenizer.from_pretrained"):
            with patch(
                "transformers.AutoModelForSequenceClassification.from_pretrained"
            ):
                self.processor = IndoBERTFashionProcessor("./fine-tuned-model")
                # Replace the model's forward method with a mock that returns quickly
                self.processor.model = MagicMock()
                outputs = MagicMock()
                outputs.logits = MagicMock()
                self.processor.model.return_value = outputs

    def test_response_generator_latency(self):
        """Test the latency of response generation"""
        print("\nTesting Response Generator Latency")

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

        latencies = []

        for params in test_params:
            start_time = time.time()
            self.response_generator.generate_response(params)
            end_time = time.time()
            latency = (end_time - start_time) * 1000  # Convert to milliseconds
            latencies.append(latency)
            print(f"  Params: {params}")
            print(f"  Latency: {latency:.2f} ms")

        avg_latency = statistics.mean(latencies)
        max_latency = max(latencies)
        min_latency = min(latencies)
        std_dev = statistics.stdev(latencies) if len(latencies) > 1 else 0

        print(f"\nResponse Generator Latency Statistics:")
        print(f"  Average: {avg_latency:.2f} ms")
        print(f"  Maximum: {max_latency:.2f} ms")
        print(f"  Minimum: {min_latency:.2f} ms")
        print(f"  Std Dev: {std_dev:.2f} ms")

        # Assert reasonable latency - adjust threshold based on your requirements
        self.assertLess(
            avg_latency, 100, "Average response generation time should be under 100ms"
        )
        self.assertLess(
            max_latency, 200, "Maximum response generation time should be under 200ms"
        )

    def test_fashion_mapping_latency(self):
        """Test the latency of fashion mapping recommendations"""
        print("\nTesting Fashion Mapping Latency")

        test_params = [
            {"gender": "pria", "skin_tone": "light", "occasion": "formal"},
            {"gender": "wanita", "skin_tone": "dark", "occasion": "casual"},
            {
                "gender": "pria",
                "skin_tone": "light",
                "occasion": "formal",
                "weather": "hot",
            },
            {
                "gender": "wanita",
                "skin_tone": "dark",
                "occasion": "casual",
                "season": "winter",
            },
            {
                "gender": "pria",
                "skin_tone": "light",
                "occasion": "formal",
                "weather": "cold",
                "season": "autumn",
            },
        ]

        latencies = []

        for params in test_params:
            start_time = time.time()
            recommendation = self.fashion_mapping.get_recommendation(params)
            formatted_response = self.fashion_mapping.format_recommendation(
                recommendation, params
            )
            end_time = time.time()
            latency = (end_time - start_time) * 1000  # Convert to milliseconds
            latencies.append(latency)
            print(f"  Params: {params}")
            print(f"  Latency: {latency:.2f} ms")

        avg_latency = statistics.mean(latencies)
        max_latency = max(latencies)
        min_latency = min(latencies)
        std_dev = statistics.stdev(latencies) if len(latencies) > 1 else 0

        print(f"\nFashion Mapping Latency Statistics:")
        print(f"  Average: {avg_latency:.2f} ms")
        print(f"  Maximum: {max_latency:.2f} ms")
        print(f"  Minimum: {min_latency:.2f} ms")
        print(f"  Std Dev: {std_dev:.2f} ms")

        # Assert reasonable latency - adjust threshold based on your requirements
        self.assertLess(avg_latency, 50, "Average mapping time should be under 50ms")
        self.assertLess(max_latency, 100, "Maximum mapping time should be under 100ms")

    def test_parameter_extraction_latency(self):
        """Test the latency of parameter extraction from text"""
        print("\nTesting Parameter Extraction Latency")

        # Approach 1: Directly measure the extract_parameters_from_intent method
        test_cases = [
            ("formal_pria_light", "Saya butuh baju formal untuk interview kerja"),
            (
                "casual_wanita_dark",
                "Outfit santai untuk jalan-jalan buat cewek kulit sawo matang",
            ),
            ("wedding", "Baju untuk pernikahan"),
            ("hot_weather", "Pakaian untuk cuaca panas di Surabaya"),
            ("summer", "Outfit untuk musim panas"),
            ("other", "Saya mau beli baju"),
        ]

        latencies = []

        for intent_name, text in test_cases:
            start_time = time.time()
            parameters = self.processor.extract_parameters_from_intent(
                intent_name, text
            )
            end_time = time.time()
            latency = (end_time - start_time) * 1000  # Convert to milliseconds
            latencies.append(latency)
            print(f"  Intent: {intent_name}, Text: '{text}'")
            print(f"  Latency: {latency:.2f} ms")
            print(f"  Parameters: {parameters}")

        avg_latency = statistics.mean(latencies)
        max_latency = max(latencies)
        min_latency = min(latencies)
        std_dev = statistics.stdev(latencies) if len(latencies) > 1 else 0

        print(f"\nParameter Extraction Latency Statistics:")
        print(f"  Average: {avg_latency:.2f} ms")
        print(f"  Maximum: {max_latency:.2f} ms")
        print(f"  Minimum: {min_latency:.2f} ms")
        print(f"  Std Dev: {std_dev:.2f} ms")

        # Assert reasonable latency - adjust threshold based on your requirements
        self.assertLess(
            avg_latency, 20, "Average parameter extraction time should be under 20ms"
        )
        self.assertLess(
            max_latency, 50, "Maximum parameter extraction time should be under 50ms"
        )

    def test_end_to_end_latency(self):
        """Test the end-to-end latency of processing a request (without speech)"""
        print("\nTesting End-to-End Processing Latency (without speech)")

        # Mock the speech components to focus on the processing latency
        with patch.object(self.processor, "classify_intent") as mock_classify:
            with patch.object(self.processor, "analyze_sentiment") as mock_sentiment:
                # Configure the mocks for deterministic behavior
                mock_classify.return_value = 0  # formal_pria_light
                mock_sentiment.return_value = 1  # positive

                test_queries = [
                    "Rekomendasi pakaian formal untuk pria",
                    "Outfit casual untuk cewek kulit sawo matang",
                    "Baju untuk ke pernikahan",
                    "Pakaian untuk cuaca panas",
                    "Baju untuk musim dingin",
                ]

                latencies = []

                for query in test_queries:
                    start_time = time.time()

                    # Simulate the processing flow without speech conversion
                    intent_id = self.processor.classify_intent(query)
                    sentiment = self.processor.analyze_sentiment(query)
                    response_text, clothing_json = self.processor.generate_response(
                        query, intent_id, sentiment
                    )

                    end_time = time.time()
                    latency = (end_time - start_time) * 1000  # Convert to milliseconds
                    latencies.append(latency)
                    print(f"  Query: '{query}'")
                    print(f"  Latency: {latency:.2f} ms")

                avg_latency = statistics.mean(latencies)
                max_latency = max(latencies)
                min_latency = min(latencies)
                std_dev = statistics.stdev(latencies) if len(latencies) > 1 else 0

                print(f"\nEnd-to-End Processing Latency Statistics (without speech):")
                print(f"  Average: {avg_latency:.2f} ms")
                print(f"  Maximum: {max_latency:.2f} ms")
                print(f"  Minimum: {min_latency:.2f} ms")
                print(f"  Std Dev: {std_dev:.2f} ms")

                # Assert reasonable latency - adjust threshold based on your requirements
                self.assertLess(
                    avg_latency,
                    150,
                    "Average end-to-end processing time should be under 150ms",
                )
                self.assertLess(
                    max_latency,
                    300,
                    "Maximum end-to-end processing time should be under 300ms",
                )


if __name__ == "__main__":
    unittest.main()
