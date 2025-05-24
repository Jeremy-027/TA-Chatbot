# src/tests/test_error_handling.py
import unittest
import os
import azure.cognitiveservices.speech as speechsdk
from unittest.mock import patch
from chatbot_azure import AzureFashionChatbot


class TestErrorHandling(unittest.TestCase):
    def setUp(self):
        self.chatbot = AzureFashionChatbot()

    @patch("azure.cognitiveservices.speech.SpeechRecognizer.recognize_once")
    def test_speech_recognition_failure(self, mock_recognize):
        """Test system's response to speech recognition failures."""
        # Mock speech recognition with "No match" result
        mock_result = speechsdk.SpeechRecognitionResult()
        mock_result._reason = speechsdk.ResultReason.NoMatch
        mock_recognize.return_value = mock_result

        result = self.chatbot.speech_to_text()
        self.assertEqual(result, "", "Should return empty string on NoMatch")

        # Mock speech recognition with "Canceled" result
        mock_result = speechsdk.SpeechRecognitionResult()
        mock_result._reason = speechsdk.ResultReason.Canceled
        mock_recognize.return_value = mock_result

        result = self.chatbot.speech_to_text()
        self.assertEqual(result, "", "Should return empty string on Canceled")

    @patch("language_model.IndoBERTFashionProcessor.classify_intent")
    def test_intent_classification_failure(self, mock_classify):
        """Test system's response to intent classification failures."""
        # Mock intent classification to raise an exception
        mock_classify.side_effect = Exception("Intent classification failed")

        response, is_error, json_data = self.chatbot.process_input("test query")

        self.assertTrue(is_error, "Should indicate an error occurred")
        self.assertIsNone(json_data, "JSON data should be None on error")
        self.assertIn("kesalahan", response.lower(), "Response should mention error")

    @patch("azure.cognitiveservices.speech.SpeechSynthesizer.speak_ssml_async")
    def test_text_to_speech_failure(self, mock_speak):
        """Test system's response to speech synthesis failures."""
        # Mock speech synthesis with "Canceled" result
        mock_result = speechsdk.SpeechSynthesisResult()
        mock_result._reason = speechsdk.ResultReason.Canceled
        mock_result._cancellation_details = speechsdk.CancellationDetails()
        mock_result._cancellation_details._reason = speechsdk.CancellationReason.Error
        mock_result._cancellation_details._error_details = "Synthesis error"

        mock_future = unittest.mock.MagicMock()
        mock_future.get.return_value = mock_result
        mock_speak.return_value = mock_future

        # Should not raise exception but log the error
        with self.assertLogs(level="ERROR") as cm:
            self.chatbot.text_to_speech("Test text")
            self.assertIn("Error", cm.output[0])
