# src/language_model.py
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import logging
from response_generator import ResponseGenerator

logger = logging.getLogger(__name__)


class IndoBERTFashionProcessor:
    def __init__(self, model_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.response_generator = ResponseGenerator()  # Add this line
        print(f"Using device: {self.device}")

        # Define categories
        self.categories = {
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

    def preprocess_text(self, text):
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=128,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        return encoding.to(self.device)

    def classify_intent(self, text):  # THIS LINE NEEDS TO BE INDENTED
        try:
            inputs = self.preprocess_text(text)
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.softmax(outputs.logits, dim=1)

                # Get top 2 predictions
                values, indices = torch.topk(predictions, 2)

                category_id = indices[0][0].item()
                confidence = values[0][0].item()

                # If confidence is too low, try to determine from keywords
                if confidence < 0.5:
                    category_id = self._keyword_fallback(text)

                print(f"\nDetected intent: {self.categories[category_id]}")
                print(f"Confidence: {confidence:.2f}")
                return category_id

        except Exception as e:
            logger.error(f"Error in intent classification: {str(e)}")
            return 19

    def _keyword_fallback(self, text):
        """Fallback method using keywords when confidence is low"""
        text = text.lower()

        # Season keywords
        if any(word in text for word in ["musim panas", "summer"]):
            return 15  # summer
        if any(word in text for word in ["musim dingin", "winter"]):
            return 16  # winter
        if any(word in text for word in ["musim semi", "spring"]):
            return 17  # spring
        if any(word in text for word in ["musim gugur", "autumn", "fall"]):
            return 18  # autumn

        # Weather keywords
        if any(word in text for word in ["panas", "gerah", "terik"]):
            return 11  # hot_weather
        if any(word in text for word in ["dingin", "sejuk"]):
            return 12  # cold_weather
        if any(word in text for word in ["hujan", "gerimis"]):
            return 13  # rainy_weather

        # Event keywords
        if "pesta" in text:
            return 9  # party
        if any(word in text for word in ["nikah", "pernikahan", "wedding"]):
            return 8  # wedding
        if any(word in text for word in ["interview", "wawancara"]):
            if "wanita" in text:
                return 1  # formal_wanita
            return 0  # formal_pria

        return 19  # other

    def analyze_sentiment(self, text):
        return 1  # Default neutral sentiment

    def generate_response(self, text, intent_id, sentiment):
        try:
            # Extract parameters from intent
            intent_name = self.categories[intent_id]

            # Parse intent to get parameters
            parameters = self.extract_parameters_from_intent(intent_name, text)

            # Use ResponseGenerator to generate the response
            text_response, clothing_json = self.response_generator.generate_response(
                parameters
            )

            return text_response, clothing_json

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "Maaf, bisakah Anda mengulangi pertanyaan Anda?", "{}"

    def extract_parameters_from_intent(self, intent_name, text):
        """Extract parameters from intent and text"""
        parameters = {}

        # Extract from intent name (e.g., "formal_pria_light")
        parts = intent_name.split("_")

        # Determine occasion
        if parts[0] in ["formal", "kasual"]:
            parameters["occasion"] = parts[0]
        elif intent_name in ["wedding", "party", "business_meeting"]:
            parameters["occasion"] = intent_name
        elif "weather" in intent_name:
            parameters["weather"] = intent_name.replace("_weather", "")
        elif intent_name in ["summer", "winter", "spring", "autumn"]:
            parameters["season"] = intent_name

        # Also check text for season mentions if not already found
        if "season" not in parameters:
            if any(word in text.lower() for word in ["musim panas", "summer"]):
                parameters["season"] = "summer"
            elif any(word in text.lower() for word in ["musim dingin", "winter"]):
                parameters["season"] = "winter"
            elif any(word in text.lower() for word in ["musim semi", "spring"]):
                parameters["season"] = "spring"
            elif any(
                word in text.lower() for word in ["musim gugur", "autumn", "fall"]
            ):
                parameters["season"] = "autumn"

        # Extract gender from intent or text
        if len(parts) > 1 and parts[1] in ["pria", "wanita"]:
            parameters["gender"] = parts[1]
        else:
            # Try to extract from text
            if any(word in text.lower() for word in ["pria", "laki-laki", "cowok"]):
                parameters["gender"] = "pria"
            elif any(word in text.lower() for word in ["wanita", "perempuan", "cewek"]):
                parameters["gender"] = "wanita"

        # Extract skin tone
        if len(parts) > 2 and parts[2] in ["light", "dark"]:
            parameters["skin_tone"] = parts[2]
        else:
            # Try to extract from text
            if any(word in text.lower() for word in ["cerah", "putih"]):
                parameters["skin_tone"] = "light"
            elif any(
                word in text.lower() for word in ["sawo matang", "gelap", "coklat"]
            ):
                parameters["skin_tone"] = "dark"

        # Set defaults if not found
        if "gender" not in parameters:
            parameters["gender"] = "neutral"
        if "skin_tone" not in parameters:
            parameters["skin_tone"] = "neutral"
        if (
            "occasion" not in parameters
            and "season" not in parameters
            and "weather" not in parameters
        ):
            parameters["occasion"] = "casual"

        return parameters
