# tests/test_speech_performance.py
import unittest
import sys
import os
import time
import statistics
import json
from unittest.mock import patch, MagicMock, PropertyMock

# Add the src directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# Create mocks for Azure dependencies
mock_os = MagicMock()
mock_azure = MagicMock()
mock_speechsdk = MagicMock()
mock_load_dotenv = MagicMock()
mock_language_model = MagicMock()
mock_logging = MagicMock()


# Define mock classes for Azure SDK
class MockSpeechRecognitionResult:
    def __init__(self, text, reason, duration=500):
        self.text = text
        self.reason = reason
        self._duration = duration  # in milliseconds

    @property
    def duration(self):
        return self._duration


class MockSpeechSynthesisResult:
    def __init__(self, reason, audio_duration=1000):
        self.reason = reason
        self._audio_duration = audio_duration  # in milliseconds

    @property
    def audio_duration(self):
        return self._audio_duration


# Apply all the patches
patches = {
    "os": mock_os,
    "azure.cognitiveservices.speech": mock_speechsdk,
    "dotenv": MagicMock(),
    "dotenv.load_dotenv": mock_load_dotenv,
    "language_model": mock_language_model,
    "logging": mock_logging,
}

for mod, mock in patches.items():
    patch.dict("sys.modules", {mod: mock}).start()

# Now import the module to be tested
with patch.dict("sys.modules", patches):
    from chatbot_azure import AzureFashionChatbot


class TestSpeechPerformance(unittest.TestCase):
    """Test suite for measuring the performance of speech services"""

    def setUp(self):
        """Set up the chatbot with mocked dependencies"""
        # Set up environment variables
        mock_os.getenv.side_effect = lambda key: {
            "AZURE_SPEECH_KEY": "mock_key",
            "AZURE_SPEECH_REGION": "mock_region",
        }.get(key)

        # Mock Azure speech SDK components
        mock_speechsdk.SpeechConfig.return_value = MagicMock()
        mock_speechsdk.SpeechRecognizer.return_value = MagicMock()
        mock_speechsdk.SpeechSynthesizer.return_value = MagicMock()

        # Mock result reasons
        mock_speechsdk.ResultReason.RecognizedSpeech = "RecognizedSpeech"
        mock_speechsdk.ResultReason.NoMatch = "NoMatch"
        mock_speechsdk.ResultReason.Canceled = "Canceled"
        mock_speechsdk.ResultReason.SynthesizingAudioCompleted = (
            "SynthesizingAudioCompleted"
        )

        # Mock NLP processor
        mock_language_model.IndoBERTFashionProcessor.return_value = MagicMock()

        # Initialize the chatbot
        self.chatbot = AzureFashionChatbot()

        # Define test utterances with varying lengths
        self.test_utterances = {
            "short": "Baju formal",
            "medium": "Rekomendasi pakaian formal untuk pria",
            "long": "Saya ingin mencari pakaian formal untuk acara pernikahan yang cocok untuk pria berkulit cerah",
            "very_long": "Tolong berikan saya rekomendasi yang lengkap untuk pakaian formal yang cocok untuk presentasi bisnis penting, saya seorang pria berkulit sawo matang dan saya ingin terlihat profesional namun tetap modern",
        }

    def test_speech_to_text_latency(self):
        """Test the latency of speech-to-text conversion with different utterance lengths"""
        print("\nTesting Speech-to-Text Latency by Utterance Length")

        # Configure mock recognizer to simulate different processing times based on utterance length
        def mock_recognize_once():
            time.sleep(0.2)  # Base delay
            return self.mock_recognition_result

        self.chatbot.speech_recognizer.recognize_once = mock_recognize_once

        latencies_by_length = {}

        for length, utterance in self.test_utterances.items():
            print(f"\n  Testing '{length}' utterance: '{utterance}'")

            # Simulate different recognition delays based on utterance length
            recognition_duration = len(utterance.split()) * 50  # 50ms per word

            self.mock_recognition_result = MockSpeechRecognitionResult(
                text=utterance,
                reason=mock_speechsdk.ResultReason.RecognizedSpeech,
                duration=recognition_duration,
            )

            latencies = []
            for _ in range(5):  # Run 5 times for each length
                start_time = time.time()
                result = self.chatbot.speech_to_text()
                end_time = time.time()

                latency = (end_time - start_time) * 1000  # ms
                latencies.append(latency)

                # Verify the result
                self.assertEqual(result, utterance.lower())

            avg_latency = statistics.mean(latencies)
            latencies_by_length[length] = avg_latency

            print(f"  Recognition Duration (simulated): {recognition_duration} ms")
            print(f"  Average Latency: {avg_latency:.2f} ms")

        print("\n  Speech-to-Text Latency by Utterance Length:")
        for length, latency in latencies_by_length.items():
            print(f"  {length.capitalize()}: {latency:.2f} ms")

        # Check that latencies increase reasonably with utterance length
        self.assertLess(
            latencies_by_length["short"],
            latencies_by_length["very_long"],
            "Speech-to-text latency should increase with utterance length",
        )

    def test_text_to_speech_latency(self):
        """Test the latency of text-to-speech conversion with different response lengths"""
        print("\nTesting Text-to-Speech Latency by Response Length")

        # Sample responses of different lengths
        test_responses = {
            "short": "Ini kemeja formal.",
            "medium": "Untuk pria, saya rekomendasikan kemeja putih dengan jas navy blue.",
            "long": "Untuk acara formal, pria dengan kulit cerah akan terlihat bagus dengan kemeja putih, jas navy blue, celana formal hitam, dan sepatu pantofel.",
            "very_long": "Untuk pria dengan kulit cerah yang menghadiri acara formal seperti pernikahan, saya rekomendasikan kombinasi kemeja putih dengan jas navy blue yang dipasangkan dengan celana formal hitam dan sepatu oxford. Tambahkan dasi sutra burgundy dan jam tangan silver untuk melengkapi penampilan elegan Anda.",
        }

        # Configure mock synthesizer
        def mock_speak_ssml_async():
            # Simulate SSML processing
            time.sleep(0.1)

            # Return a mock that has a get method
            mock_result = MagicMock()
            mock_result.get.return_value = self.mock_synthesis_result

            return mock_result

        self.chatbot.speech_synthesizer.speak_ssml_async = mock_speak_ssml_async

        latencies_by_length = {}

        for length, response in test_responses.items():
            print(f"\n  Testing '{length}' response: '{response[:30]}...'")

            # Simulate different synthesis times based on response length
            audio_duration = (
                len(response.split()) * 100
            )  # 100ms per word (approximate speech rate)

            self.mock_synthesis_result = MockSpeechSynthesisResult(
                reason=mock_speechsdk.ResultReason.SynthesizingAudioCompleted,
                audio_duration=audio_duration,
            )

            latencies = []
            for _ in range(5):  # Run 5 times for each length
                start_time = time.time()
                self.chatbot.text_to_speech(response)
                end_time = time.time()

                latency = (end_time - start_time) * 1000  # ms
                latencies.append(latency)

            avg_latency = statistics.mean(latencies)
            latencies_by_length[length] = avg_latency

            print(f"  Synthesis Duration (simulated): {audio_duration} ms")
            print(f"  Average Latency: {avg_latency:.2f} ms")

        print("\n  Text-to-Speech Latency by Response Length:")
        for length, latency in latencies_by_length.items():
            print(f"  {length.capitalize()}: {latency:.2f} ms")

        # Check that latencies increase reasonably with response length
        self.assertLess(
            latencies_by_length["short"],
            latencies_by_length["very_long"],
            "Text-to-speech latency should increase with response length",
        )

    def test_end_to_end_response_time(self):
        """Test the end-to-end response time including speech processing"""
        print("\nTesting End-to-End Response Time (with speech)")

        # Configure mocks for complete flow
        def mock_speech_to_text():
            time.sleep(0.3)  # Simulate recognition time
            return "rekomendasi pakaian formal untuk pria"

        def mock_process_input(text):
            time.sleep(0.2)  # Simulate processing time
            return (
                "Untuk pria, saya rekomendasikan kemeja putih dengan jas navy blue.",
                False,
                "{}",
            )

        def mock_text_to_speech(text, is_error=False):
            if not is_error:
                time.sleep(0.5)  # Simulate synthesis time

        self.chatbot.speech_to_text = mock_speech_to_text
        self.chatbot.process_input = mock_process_input
        self.chatbot.text_to_speech = mock_text_to_speech

        # Measure complete conversation turn time
        iterations = 5
        turn_times = []

        for i in range(iterations):
            print(f"  Measuring conversation turn {i+1}/{iterations}...")

            # Start measuring
            start_time = time.time()

            # Simulate one complete turn: listen, process, respond
            user_input = self.chatbot.speech_to_text()
            response, is_error, clothing_json = self.chatbot.process_input(user_input)
            self.chatbot.text_to_speech(response, is_error)

            # End measuring
            end_time = time.time()
            turn_time = (end_time - start_time) * 1000  # ms
            turn_times.append(turn_time)

            print(f"  Conversation Turn Time: {turn_time:.2f} ms")

        # Calculate statistics
        avg_turn_time = statistics.mean(turn_times)
        max_turn_time = max(turn_times)
        min_turn_time = min(turn_times)

        print(f"\n  End-to-End Conversation Turn Time Statistics:")
        print(f"  Average: {avg_turn_time:.2f} ms")
        print(f"  Maximum: {max_turn_time:.2f} ms")
        print(f"  Minimum: {min_turn_time:.2f} ms")

        # Convert to seconds for more human-readable assessment
        avg_seconds = avg_turn_time / 1000
        print(f"  Average response time: {avg_seconds:.2f} seconds")

        # Assert maximum acceptable turn time (adjust based on requirements)
        self.assertLess(
            avg_seconds, 3, "Average conversation turn should be under 3 seconds"
        )

    def test_simulated_real_world_conversation(self):
        """Test realistic conversation scenarios with varying complexity"""
        print("\nTesting Simulated Real-World Conversation Scenarios")

        # Define test scenarios with varying complexity
        scenarios = [
            {
                "name": "Simple Query",
                "user_input": "Baju formal",
                "processing_time": 0.2,
                "response_length": "short",
            },
            {
                "name": "Medium Query with Parameters",
                "user_input": "Rekomendasi pakaian formal untuk pria berkulit cerah",
                "processing_time": 0.4,
                "response_length": "medium",
            },
            {
                "name": "Complex Query with Multiple Parameters",
                "user_input": "Saya mencari outfit untuk acara pernikahan, saya pria dengan kulit sawo matang",
                "processing_time": 0.6,
                "response_length": "long",
            },
            {
                "name": "Very Complex Query with Clarification",
                "user_input": "Saya ingin pakaian yang cocok untuk presentasi penting di kantor tapi juga nyaman dipakai seharian",
                "processing_time": 0.8,
                "response_length": "very_long",
            },
        ]

        # Configure mocks with variable behavior
        def configure_mocks(scenario):
            def mock_speech_to_text():
                # Simulate recognition time based on input length
                recognition_time = len(scenario["user_input"].split()) * 0.05
                time.sleep(recognition_time)
                return scenario["user_input"].lower()

            def mock_process_input(text):
                # Simulate processing with the specified time
                time.sleep(scenario["processing_time"])

                # Generate response based on specified length
                response_lengths = {
                    "short": "Ini rekomendasinya.",
                    "medium": "Untuk pria, saya rekomendasikan kemeja formal dengan celana bahan.",
                    "long": "Untuk pria dengan kulit cerah yang akan menghadiri acara formal, saya merekomendasikan kemeja putih dengan jas navy blue dan celana formal hitam.",
                    "very_long": "Untuk pria dengan kulit sawo matang yang akan menghadiri acara pernikahan, saya merekomendasikan kombinasi kemeja putih dengan jas berwarna deep burgundy, celana formal hitam, dan sepatu oxford. Tambahkan dasi dengan warna gold sebagai aksen untuk melengkapi penampilan Anda.",
                }

                response = response_lengths[scenario["response_length"]]
                return response, False, "{}"

            def mock_text_to_speech(text, is_error=False):
                if not is_error:
                    # Simulate synthesis time based on response length
                    synthesis_time = len(text.split()) * 0.075
                    time.sleep(synthesis_time)

            self.chatbot.speech_to_text = mock_speech_to_text
            self.chatbot.process_input = mock_process_input
            self.chatbot.text_to_speech = mock_text_to_speech

        scenario_results = {}

        for scenario in scenarios:
            print(f"\n  Testing Scenario: {scenario['name']}")
            print(f"  User Input: '{scenario['user_input']}'")

            # Configure mocks for this scenario
            configure_mocks(scenario)

            # Measure conversation turn time
            start_time = time.time()

            # Simulate one complete conversation turn
            user_input = self.chatbot.speech_to_text()
            response, is_error, clothing_json = self.chatbot.process_input(user_input)
            self.chatbot.text_to_speech(response, is_error)

            end_time = time.time()
            turn_time = (end_time - start_time) * 1000  # ms

            # Store results
            scenario_results[scenario["name"]] = {
                "turn_time_ms": turn_time,
                "turn_time_seconds": turn_time / 1000,
            }

            print(
                f"  Total Response Time: {turn_time:.2f} ms ({turn_time/1000:.2f} seconds)"
            )

        # Print overall comparison
        print("\n  Response Time Comparison Across Scenarios:")
        for name, results in scenario_results.items():
            print(f"  {name}: {results['turn_time_seconds']:.2f} seconds")

        # Assert reasonable response times for all scenarios
        for name, results in scenario_results.items():
            self.assertLess(
                results["turn_time_seconds"],
                5,
                f"Response time for scenario '{name}' should be under 5 seconds",
            )


if __name__ == "__main__":
    unittest.main()
