# tests/test_chatbot_azure.py
import unittest
import sys
import os
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
    def __init__(self, text, reason):
        self.text = text
        self.reason = reason


class MockSpeechSynthesisResult:
    def __init__(self, reason):
        self.reason = reason


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


class TestAzureFashionChatbot(unittest.TestCase):
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

        # Mock cancellation details
        mock_speechsdk.CancellationDetails.return_value = MagicMock()
        mock_speechsdk.CancellationReason.Error = "Error"

        # Mock NLP processor
        mock_language_model.IndoBERTFashionProcessor.return_value = MagicMock()

        # Initialize the chatbot
        self.chatbot = AzureFashionChatbot()

    def test_initialization(self):
        """Test that chatbot initializes correctly with Azure services"""
        # Verify environment variables were accessed
        mock_os.getenv.assert_any_call("AZURE_SPEECH_KEY")
        mock_os.getenv.assert_any_call("AZURE_SPEECH_REGION")

        # Verify speech config was created
        mock_speechsdk.SpeechConfig.assert_called_with(
            subscription="mock_key", region="mock_region"
        )

        # Verify language settings
        self.assertEqual(
            self.chatbot.speech_config.speech_recognition_language, "id-ID"
        )
        self.assertEqual(self.chatbot.speech_config.speech_synthesis_language, "id-ID")
        self.assertEqual(
            self.chatbot.speech_config.speech_synthesis_voice_name, "id-ID-GadisNeural"
        )

        # Verify recognizer and synthesizer were created
        mock_speechsdk.SpeechRecognizer.assert_called_with(
            speech_config=self.chatbot.speech_config
        )
        mock_speechsdk.SpeechSynthesizer.assert_called_with(
            speech_config=self.chatbot.speech_config
        )

        # Verify NLP processor was initialized
        mock_language_model.IndoBERTFashionProcessor.assert_called_with(
            model_path="./fine-tuned-model"
        )

    def test_speech_to_text_successful(self):
        """Test successful speech-to-text conversion"""
        # Mock a successful recognition
        mock_result = MockSpeechRecognitionResult(
            text="Rekomendasi pakaian formal untuk pria",
            reason=mock_speechsdk.ResultReason.RecognizedSpeech,
        )
        self.chatbot.speech_recognizer.recognize_once.return_value = mock_result

        # Call the speech_to_text method
        result = self.chatbot.speech_to_text()

        # Verify the result
        self.assertEqual(result, "rekomendasi pakaian formal untuk pria")

    def test_speech_to_text_no_match(self):
        """Test speech-to-text with no recognition match"""
        # Mock a no-match result
        mock_result = MockSpeechRecognitionResult(
            text="", reason=mock_speechsdk.ResultReason.NoMatch
        )
        self.chatbot.speech_recognizer.recognize_once.return_value = mock_result

        # Call the speech_to_text method
        result = self.chatbot.speech_to_text()

        # Verify the result
        self.assertEqual(result, "")

    def test_speech_to_text_canceled(self):
        """Test speech-to-text with canceled recognition"""
        # Mock a canceled result
        mock_result = MockSpeechRecognitionResult(
            text="", reason=mock_speechsdk.ResultReason.Canceled
        )
        self.chatbot.speech_recognizer.recognize_once.return_value = mock_result

        # Call the speech_to_text method
        result = self.chatbot.speech_to_text()

        # Verify the result
        self.assertEqual(result, "")

    def test_speech_to_text_exception(self):
        """Test speech-to-text with an exception"""
        # Mock an exception
        self.chatbot.speech_recognizer.recognize_once.side_effect = Exception(
            "Test error"
        )

        # Call the speech_to_text method
        result = self.chatbot.speech_to_text()

        # Verify the result
        self.assertEqual(result, "")

    def test_text_to_speech_successful(self):
        """Test successful text-to-speech conversion"""
        # Mock a successful synthesis
        mock_result = MockSpeechSynthesisResult(
            reason=mock_speechsdk.ResultReason.SynthesizingAudioCompleted
        )
        self.chatbot.speech_synthesizer.speak_ssml_async().get.return_value = (
            mock_result
        )

        # Test text and expected SSML
        test_text = "Ini adalah tes text-to-speech"
        expected_ssml = f"""
            <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="id-ID">
                <voice name="id-ID-GadisNeural">
                    {test_text}
                </voice>
            </speak>
            """

        # Call the text_to_speech method
        self.chatbot.text_to_speech(test_text)

        # Verify the synthesizer was called with the correct SSML
        self.chatbot.speech_synthesizer.speak_ssml_async.assert_called_with(
            expected_ssml
        )

    def test_text_to_speech_error(self):
        """Test text-to-speech with an error"""
        # Mock a synthesis error
        mock_result = MockSpeechSynthesisResult(
            reason=mock_speechsdk.ResultReason.Canceled
        )
        self.chatbot.speech_synthesizer.speak_ssml_async().get.return_value = (
            mock_result
        )

        # Mock cancellation details
        mock_result.cancellation_details = MagicMock()
        mock_result.cancellation_details.reason = (
            mock_speechsdk.CancellationReason.Error
        )
        mock_result.cancellation_details.error_details = "Test error details"

        # Call the text_to_speech method
        self.chatbot.text_to_speech("Test text")

        # Verify error details were accessed
        self.assertEqual(
            mock_result.cancellation_details.reason,
            mock_speechsdk.CancellationReason.Error,
        )

    def test_text_to_speech_is_error(self):
        """Test text-to-speech with is_error flag"""
        # Call the text_to_speech method with is_error=True
        self.chatbot.text_to_speech("Error message", is_error=True)

        # Verify the synthesizer was not called
        self.chatbot.speech_synthesizer.speak_ssml_async.assert_not_called()

    def test_process_input_empty(self):
        """Test processing empty input"""
        # Call the process_input method with empty input
        response, is_error, clothing_json = self.chatbot.process_input("")

        # Verify the response
        self.assertEqual(response, "Maaf, bisakah Anda mengulangi?")
        self.assertTrue(is_error)
        self.assertIsNone(clothing_json)

    def test_process_input_exit_commands(self):
        """Test processing exit commands"""
        exit_commands = ["keluar", "selesai", "quit", "exit", "stop"]

        for command in exit_commands:
            # Call the process_input method with exit command
            response, is_error, clothing_json = self.chatbot.process_input(command)

            # Verify the response
            self.assertEqual(response, "KELUAR")
            self.assertFalse(is_error)
            self.assertIsNone(clothing_json)

    def test_process_input_valid(self):
        """Test processing valid input"""
        # Mock the NLP processor's response
        test_text = "Rekomendasi pakaian formal untuk pria"
        mock_intent_id = 0  # formal_pria_light
        mock_sentiment = 1  # positive
        mock_text_response = "Untuk pria dengan kulit cerah yang akan menghadiri acara formal, saya merekomendasikan jas navy blue dengan kemeja putih."
        mock_clothing_json = (
            '{"clothing": {"top": "jas navy blue", "bottom": "celana formal hitam"}}'
        )

        self.chatbot.nlp_processor.classify_intent.return_value = mock_intent_id
        self.chatbot.nlp_processor.analyze_sentiment.return_value = mock_sentiment
        self.chatbot.nlp_processor.generate_response.return_value = (
            mock_text_response,
            mock_clothing_json,
        )

        # Call the process_input method
        response, is_error, clothing_json = self.chatbot.process_input(test_text)

        # Verify the NLP processor methods were called
        self.chatbot.nlp_processor.classify_intent.assert_called_with(test_text)
        self.chatbot.nlp_processor.analyze_sentiment.assert_called_with(test_text)
        self.chatbot.nlp_processor.generate_response.assert_called_with(
            test_text, mock_intent_id, mock_sentiment
        )

        # Verify the response
        self.assertEqual(response, mock_text_response)
        self.assertFalse(is_error)
        self.assertEqual(clothing_json, mock_clothing_json)

    def test_process_input_exception(self):
        """Test processing input with an exception"""
        # Mock an exception in the NLP processor
        test_text = "This will cause an error"
        self.chatbot.nlp_processor.classify_intent.side_effect = Exception("Test error")

        # Call the process_input method
        response, is_error, clothing_json = self.chatbot.process_input(test_text)

        # Verify the response
        self.assertIn("Maaf, terjadi kesalahan", response)
        self.assertTrue(is_error)
        self.assertIsNone(clothing_json)

    @patch("builtins.print")
    @patch("builtins.open")
    def test_run_method(self, mock_open, mock_print):
        """Test the main run method"""
        # Mock speech-to-text to return specific inputs in sequence
        self.chatbot.speech_to_text = MagicMock()
        self.chatbot.speech_to_text.side_effect = [
            "Rekomendasi pakaian formal",  # First user input
            "keluar",  # Exit command
        ]

        # Mock process_input responses
        self.chatbot.process_input = MagicMock()
        mock_clothing_json = '{"clothing": {"top": "jas navy blue"}}'

        # First call - normal response
        self.chatbot.process_input.side_effect = [
            (
                "Untuk acara formal, saya merekomendasikan jas navy blue.",
                False,
                mock_clothing_json,
            ),
            ("KELUAR", False, None),
        ]

        # Mock text-to-speech
        self.chatbot.text_to_speech = MagicMock()

        # Call the run method
        self.chatbot.run()

        # Verify welcome message was spoken
        self.chatbot.text_to_speech.assert_any_call(
            "Halo! Saya asisten fashion Anda. Apa jenis pakaian yang Anda cari?"
        )

        # Verify response was processed correctly
        self.chatbot.process_input.assert_any_call("Rekomendasi pakaian formal")

        # Verify clothing JSON was printed
        mock_print.assert_any_call("\nOutput JSON for 3D visualization:")
        mock_print.assert_any_call(mock_clothing_json)

        # Verify farewell message was spoken
        self.chatbot.text_to_speech.assert_any_call(
            "Terima kasih telah menggunakan Fashion Chatbot. Sampai jumpa!"
        )


if __name__ == "__main__":
    unittest.main()
