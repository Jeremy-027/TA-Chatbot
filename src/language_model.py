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


def classify_intent(self, text):
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

        return 19  # oth

    def analyze_sentiment(self, text):
        return 1  # Default neutral sentiment

    def generate_response(self, text, intent, sentiment):
        try:
            # Predefined responses based on intent
            responses = {
                0: "Untuk pria berkulit cerah, kenakan setelan jas navy blue dengan kemeja putih dan sepatu pantofel hitam.",
                1: "Untuk wanita berkulit cerah, kenakan blazer dengan rok pensil dan sepatu heels.",
                2: "Untuk pria berkulit sawo matang, gunakan setelan jas abu-abu dengan dasi merah dan sepatu pantofel hitam.",
                3: "Untuk wanita berkulit sawo matang, gunakan setelan blazer pastel dengan rok midi dan sepatu hak tinggi.",
                4: "Untuk pria berkulit cerah, kenakan kaos dengan jeans dan sneakers casual.",
                5: "Untuk wanita berkulit cerah, kenakan dress casual dengan flat shoes nyaman.",
                6: "Untuk pria berkulit sawo matang, gunakan t-shirt hitam dengan jeans biru dan sneakers putih.",
                7: "Untuk wanita berkulit sawo matang, kombinasikan blouse casual dengan celana jeans dan sepatu flat.",
                8: "Untuk acara pernikahan, kenakan gaun panjang dengan heels dan clutch bag.",
                9: "Untuk pesta, kenakan dress party dengan aksesoris berkilau.",
                10: "Untuk rapat bisnis, gunakan setelan jas abu-abu dengan kemeja putih.",
                11: "Untuk cuaca panas, kenakan pakaian berbahan katun yang menyerap keringat.",
                12: "Untuk cuaca dingin, kenakan sweater tebal dengan celana panjang.",
                13: "Untuk cuaca hujan, kenakan jas hujan dengan sepatu anti air.",
                14: "Untuk cuaca berangin, kenakan jaket windbreaker dengan celana panjang.",
                15: "Untuk musim panas, kenakan kaos ringan dengan celana pendek dan sandal.",
                16: "Untuk musim dingin, kenakan jaket tebal dengan celana wool.",
                17: "Untuk musim semi, kenakan dress floral dengan cardigan ringan.",
                18: "Untuk musim gugur, kenakan sweater rajut dengan celana panjang.",
                19: "Pilih pakaian yang sesuai dengan acara dan nyaman digunakan.",
            }

            return responses.get(
                intent,
                "Maaf, bisakah Anda menjelaskan lebih detail tentang jenis pakaian yang Anda cari?",
            )

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "Maaf, bisakah Anda mengulangi pertanyaan Anda?"
