# tests/test_language_model.py
import unittest
import sys
import os
import json
import numpy as np
from unittest.mock import patch, MagicMock, Mock

# Add the src directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# Create mocks for dependencies
mock_torch = MagicMock()
mock_transformers = MagicMock()
mock_tokenizer = MagicMock()
mock_model = MagicMock()
mock_response_generator = MagicMock()

# Set up patch dictionary for dependencies
patches = {
    "torch": mock_torch,
    "transformers": mock_transformers,
    "transformers.AutoTokenizer": mock_tokenizer,
    "transformers.AutoModelForSequenceClassification": mock_model,
    "response_generator.ResponseGenerator": mock_response_generator,
}

# Apply all the patches
for mod, mock in patches.items():
    patch.dict("sys.modules", {mod: mock}).start()

# Now import the module to be tested
from language_model import IndoBERTFashionProcessor


class TestIndoBERTFashionProcessor(unittest.TestCase):
    def setUp(self):
        """Set up IndoBERTFashionProcessor with mocked dependencies"""
        # Create mock return values for model and tokenizer
        self.mock_tokenizer_instance = MagicMock()
        self.mock_model_instance = MagicMock()
        self.mock_device = mock_torch.device.return_value
        self.mock_response_generator_instance = MagicMock()

        # Set up the model's prediction behavior
        outputs = MagicMock()
        outputs.logits = Mock()
        self.mock_model_instance.return_value = outputs
        mock_torch.softmax.return_value = mock_torch.tensor([[0.8, 0.1, 0.1]])
        mock_torch.topk.return_value = (
            mock_torch.tensor([[0.8, 0.1]]),
            mock_torch.tensor([[0, 1]]),
        )

        # Create the processor with mocked components
        with patch(
            "transformers.AutoTokenizer.from_pretrained",
            return_value=self.mock_tokenizer_instance,
        ):
            with patch(
                "transformers.AutoModelForSequenceClassification.from_pretrained",
                return_value=self.mock_model_instance,
            ):
                with patch("torch.device", return_value=mock_torch.device("cpu")):
                    with patch(
                        "response_generator.ResponseGenerator",
                        return_value=self.mock_response_generator_instance,
                    ):
                        self.processor = IndoBERTFashionProcessor("mock_model_path")

        # Set up the categories for testing
        self.processor.categories = {
            0: "formal_pria_light",
            1: "formal_wanita_light",
            2: "formal_pria_dark",
            3: "formal_wanita_dark",
            4: "kasual_pria_light",
            5: "kasual_wanita_light",
            6: "kasual_pria_dark",
            7: "kasual_wanita_dark",
            8: "wedding",
            9: "party",
            10: "business_meeting",
            11: "hot_weather",
            12: "cold_weather",
            13: "rainy_weather",
            14: "windy_weather",
            15: "summer",
            16: "winter",
            17: "spring",
            18: "autumn",
            19: "other",
        }

    def test_initialization(self):
        """Test that processor initializes correctly"""
        self.assertEqual(self.processor.device, self.mock_device)
        self.assertEqual(self.processor.tokenizer, self.mock_tokenizer_instance)
        self.assertEqual(self.processor.model, self.mock_model_instance)
        self.assertEqual(
            self.processor.response_generator, self.mock_response_generator_instance
        )

    def test_preprocess_text(self):
        """Test text preprocessing"""
        test_text = "Pakaian formal untuk pria"

        # Configure mock tokenizer behavior
        mock_encoding = MagicMock()
        self.mock_tokenizer_instance.return_value = mock_encoding
        mock_encoding.to.return_value = "mocked_encoded_text"

        # Call the preprocess method
        result = self.processor.preprocess_text(test_text)

        # Verify tokenizer was called with correct parameters
        self.mock_tokenizer_instance.assert_called_with(
            test_text,
            add_special_tokens=True,
            max_length=128,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )

        # Verify the encoding was moved to the correct device
        mock_encoding.to.assert_called_with(self.mock_device)

        # Verify the result
        self.assertEqual(result, "mocked_encoded_text")

    @patch("torch.no_grad", return_value=MagicMock().__enter__.return_value)
    @patch("torch.softmax")
    @patch("torch.topk")
    def test_classify_intent_high_confidence(self, mock_topk, mock_softmax, _):
        """Test intent classification with high confidence"""
        test_text = "Pakaian formal untuk pria berkulit cerah"

        # Configure mocks for classification
        mock_inputs = MagicMock()
        mock_outputs = MagicMock()
        mock_predictions = MagicMock()
        mock_values = mock_torch.tensor([[0.9, 0.1]])
        mock_indices = mock_torch.tensor([[0, 1]])

        # Set up the behavior
        with patch.object(self.processor, "preprocess_text", return_value=mock_inputs):
            self.mock_model_instance.return_value = mock_outputs
            mock_softmax.return_value = mock_predictions
            mock_topk.return_value = (mock_values, mock_indices)

            # Mock the tensor item access to return a Python int
            mock_indices[0][0].item.return_value = 0
            mock_values[0][0].item.return_value = 0.9

            # Call the classify_intent method
            intent_id = self.processor.classify_intent(test_text)

            # Verify the model and transforms were called correctly
            self.mock_model_instance.assert_called_with(**mock_inputs)
            mock_softmax.assert_called_with(mock_outputs.logits, dim=1)
            mock_topk.assert_called_with(mock_predictions, 2)

            # Verify the result
            self.assertEqual(intent_id, 0)  # Should be "formal_pria_light"

    @patch("torch.no_grad", return_value=MagicMock().__enter__.return_value)
    @patch("torch.softmax")
    @patch("torch.topk")
    def test_classify_intent_low_confidence(self, mock_topk, mock_softmax, _):
        """Test intent classification with low confidence triggering keyword fallback"""
        test_text = "Pakaian untuk musim panas"

        # Configure mocks for classification with low confidence
        mock_inputs = MagicMock()
        mock_outputs = MagicMock()
        mock_predictions = MagicMock()
        mock_values = mock_torch.tensor([[0.3, 0.2]])
        mock_indices = mock_torch.tensor([[19, 1]])  # "other" category

        # Set up the behavior
        with patch.object(self.processor, "preprocess_text", return_value=mock_inputs):
            with patch.object(
                self.processor, "_keyword_fallback", return_value=15
            ):  # summer
                self.mock_model_instance.return_value = mock_outputs
                mock_softmax.return_value = mock_predictions
                mock_topk.return_value = (mock_values, mock_indices)

                # Mock the tensor item access to return a Python int
                mock_indices[0][0].item.return_value = 19
                mock_values[0][0].item.return_value = 0.3

                # Call the classify_intent method
                intent_id = self.processor.classify_intent(test_text)

                # Verify the result should come from keyword fallback
                self.assertEqual(intent_id, 15)  # Should be "summer"

    def test_keyword_fallback(self):
        """Test the keyword fallback method for intent detection"""
        # Test seasonal keywords
        self.assertEqual(
            self.processor._keyword_fallback("outfit untuk musim panas"), 15
        )  # summer
        self.assertEqual(
            self.processor._keyword_fallback("baju untuk musim dingin"), 16
        )  # winter
        self.assertEqual(
            self.processor._keyword_fallback("pakaian musim semi"), 17
        )  # spring
        self.assertEqual(
            self.processor._keyword_fallback("rekomendasi untuk musim gugur"), 18
        )  # autumn

        # Test weather keywords
        self.assertEqual(
            self.processor._keyword_fallback("baju untuk cuaca panas"), 11
        )  # hot_weather
        self.assertEqual(
            self.processor._keyword_fallback("pakaian saat cuaca dingin"), 12
        )  # cold_weather
        self.assertEqual(
            self.processor._keyword_fallback("outfit untuk hujan"), 13
        )  # rainy_weather

        # Test event keywords
        self.assertEqual(self.processor._keyword_fallback("baju pesta"), 9)  # party
        self.assertEqual(
            self.processor._keyword_fallback("outfit untuk pernikahan"), 8
        )  # wedding
        self.assertEqual(
            self.processor._keyword_fallback("pakaian untuk interview wanita"), 1
        )  # formal_wanita
        self.assertEqual(
            self.processor._keyword_fallback("baju untuk wawancara"), 0
        )  # formal_pria

        # Test default case
        self.assertEqual(self.processor._keyword_fallback("query random"), 19)  # other

    def test_extract_parameters_from_intent(self):
        """Test extracting parameters from intent and text"""
        # Test formal intent
        intent_name = "formal_pria_light"
        text = "Saya butuh baju formal untuk interview kerja"
        parameters = self.processor.extract_parameters_from_intent(intent_name, text)

        self.assertEqual(parameters["occasion"], "formal")
        self.assertEqual(parameters["gender"], "pria")
        self.assertEqual(parameters["skin_tone"], "light")

        # Test seasonal intent
        intent_name = "summer"
        text = "Rekomendasi untuk musim panas buat pria"
        parameters = self.processor.extract_parameters_from_intent(intent_name, text)

        self.assertEqual(parameters["season"], "summer")
        self.assertEqual(parameters["gender"], "pria")

        # Test weather intent
        intent_name = "hot_weather"
        text = "Pakaian untuk cuaca panas buat wanita berkulit gelap"
        parameters = self.processor.extract_parameters_from_intent(intent_name, text)

        self.assertEqual(parameters["weather"], "hot")
        self.assertEqual(parameters["gender"], "wanita")
        self.assertEqual(parameters["skin_tone"], "dark")

        # Test default parameters
        intent_name = "other"
        text = "Baju bagus"
        parameters = self.processor.extract_parameters_from_intent(intent_name, text)

        self.assertEqual(parameters["gender"], "neutral")
        self.assertEqual(parameters["skin_tone"], "neutral")
        self.assertEqual(parameters["occasion"], "casual")

    def test_generate_response(self):
        """Test the complete response generation process"""
        test_text = "Rekomendasi pakaian formal untuk pria berkulit cerah"
        intent_id = 0  # formal_pria_light
        sentiment = 1  # positive

        # Mock response generation
        mock_params = {"gender": "pria", "skin_tone": "light", "occasion": "formal"}
        mock_text_response = "Untuk pria dengan kulit cerah yang akan menghadiri acara formal, saya merekomendasikan jas navy blue dengan kemeja putih dan dasi burgundy."
        mock_clothing_json = (
            '{"clothing": {"top": "jas navy blue", "bottom": "celana formal hitam"}}'
        )

        with patch.object(
            self.processor, "extract_parameters_from_intent", return_value=mock_params
        ):
            self.mock_response_generator_instance.generate_response.return_value = (
                mock_text_response,
                mock_clothing_json,
            )

            # Call the generate_response method
            response_text, clothing_json = self.processor.generate_response(
                test_text, intent_id, sentiment
            )

            # Verify correct parameters were extracted and passed to response generator
            self.processor.extract_parameters_from_intent.assert_called_with(
                "formal_pria_light", test_text
            )
            self.mock_response_generator_instance.generate_response.assert_called_with(
                mock_params
            )

            # Verify results
            self.assertEqual(response_text, mock_text_response)
            self.assertEqual(clothing_json, mock_clothing_json)

    def test_error_handling(self):
        """Test error handling during response generation"""
        test_text = "This will cause an error"
        intent_id = 19  # other
        sentiment = 1  # positive

        # Mock to raise an exception
        with patch.object(
            self.processor,
            "extract_parameters_from_intent",
            side_effect=Exception("Test error"),
        ):
            # Call the generate_response method
            response_text, clothing_json = self.processor.generate_response(
                test_text, intent_id, sentiment
            )

            # Verify fallback response is returned
            self.assertIn("Maaf", response_text)
            self.assertEqual(clothing_json, "{}")


if __name__ == "__main__":
    unittest.main()
