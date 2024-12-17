# src/language_model.py
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
import logging

logger = logging.getLogger(__name__)


class IndoBERTFashionProcessor:
    def __init__(self, model_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

        self.categories = {
            0: "formal_pria",
            1: "formal_wanita",
            2: "kasual_pria",
            3: "kasual_wanita",
            4: "wedding",
            5: "party",
            6: "business_meeting",
            7: "casual_outing",
            8: "hot_weather",
            9: "cold_weather",
            10: "rainy_weather",
            11: "windy_weather",
            12: "summer",
            13: "winter",
            14: "spring",
            15: "autumn",
            16: "jackets",
            17: "shoes",
            18: "accessories",
            19: "other",
        }

        self.responses = {
            "formal_pria": [
                "Untuk acara formal, saya rekomendasikan setelan jas navy blue dengan kemeja putih.",
                "Kenakan kemeja putih dengan celana bahan hitam dan sepatu pantofel.",
                "Kombinasikan blazer dengan kemeja polos dan celana bahan.",
            ],
            "formal_wanita": [
                "Untuk acara formal, saya sarankan blazer dengan rok pensil atau celana bahan.",
                "Kenakan blus formal dengan rok atau celana bahan.",
                "Padukan blazer dengan dress formal dan sepatu hak.",
            ],
            "business_meeting": [
                "Untuk meeting, kenakan setelan jas dengan dasi dan sepatu formal.",
                "Padukan blazer navy dengan kemeja light blue dan celana bahan.",
                "Kenakan kemeja lengan panjang dengan celana bahan dan sepatu formal.",
            ],
            "kasual_pria": [
                "Untuk kasual, coba kenakan polo shirt dengan chino pants.",
                "Kombinasikan kemeja casual dengan jeans dan sneakers.",
                "Kenakan t-shirt dengan celana pendek dan sepatu casual.",
            ],
            "kasual_wanita": [
                "Untuk kasual, kenakan blus dengan jeans dan flat shoes.",
                "Padukan dress casual dengan cardigan dan sneakers.",
                "Kombinasikan kaos dengan rok A-line dan sepatu nyaman.",
            ],
            "wedding": [
                "Untuk pernikahan, saya sarankan dress formal dengan warna pastel dan sepatu hak tinggi.",
                "Kenakan setelan jas dengan dasi dan sepatu formal untuk pernikahan.",
                "Padukan gaun panjang dengan clutch dan perhiasan minimalis.",
            ],
            "party": [
                "Untuk pesta, coba kenakan dress berwarna cerah dengan aksesoris yang mencolok.",
                "Kenakan kemeja kasual dengan celana jeans dan sepatu sneakers untuk pesta santai.",
                "Padukan blus berkilau dengan rok atau celana hitam untuk pesta malam.",
            ],
            "other": [
                "Untuk acara tersebut, saya sarankan pakaian yang rapi dan nyaman seperti kemeja dengan celana bahan.",
                "Kenakan pakaian yang sesuai dengan formalitas acara, seperti blazer dengan kemeja dan celana bahan.",
                "Padukan atasan dan bawahan yang senada dengan sepatu yang sesuai acara.",
            ],
        }

    def classify_intent(self, text):
        try:
            inputs = self.preprocess_text(text)
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.softmax(outputs.logits, dim=1)
                category_id = torch.argmax(predictions, dim=1).item()
                confidence = predictions[0][category_id].item()

                # Debug print
                print(
                    f"Detected intent: {self.categories.get(category_id)} (confidence: {confidence:.2f})"
                )

                return self.categories.get(category_id, "other")
        except Exception as e:
            logger.error(f"Error in intent classification: {str(e)}")
            return "other"

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

    def analyze_sentiment(self, text):
        # For simplicity, return neutral sentiment
        return 1

    def generate_response(self, text, intent, sentiment):
        try:
            # Debug print
            print(f"Generating response for intent: {intent}")

            # Check if we have specific responses for this intent
            if intent in self.responses:
                return np.random.choice(self.responses[intent])

            # Map similar intents
            intent_mapping = {
                "seminar": "formal_pria",
                "meeting": "business_meeting",
                "presentasi": "business_meeting",
                "interview": "formal_pria",
            }

            # Check for keywords in the text and map to appropriate intent
            for keyword, mapped_intent in intent_mapping.items():
                if keyword in text.lower() and mapped_intent in self.responses:
                    return np.random.choice(self.responses[mapped_intent])

            # If no specific response is found, return a default response
            return np.random.choice(self.responses["other"])

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "Maaf, bisakah Anda mengulangi pertanyaan Anda?"
