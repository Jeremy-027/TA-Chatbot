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
        self.response_generator = ResponseGenerator()

        self.categories = {
            # Formal Categories - Light Skin
            0: "formal_pria_light",
            1: "formal_wanita_light",
            # Formal Categories - Dark Skin
            2: "formal_pria_dark",
            3: "formal_wanita_dark",
            # Casual Categories - Light Skin
            4: "kasual_pria_light",
            5: "kasual_wanita_light",
            # Casual Categories - Dark Skin
            6: "kasual_pria_dark",
            7: "kasual_wanita_dark",
            # General Event Categories
            8: "wedding",
            9: "party",
            10: "business_meeting",
            # Weather Categories
            11: "hot_weather",
            12: "cold_weather",
            13: "rainy_weather",
            14: "windy_weather",
            # Season Categories
            15: "summer",
            16: "winter",
            17: "spring",
            18: "autumn",
            # Other Categories
            19: "other",
        }

        self.responses = {
            "formal_pria_light": [
                "untuk pria berkulit cerah, kenakan setelan jas navy blue dengan kemeja putih - warna gelap akan memberikan kontras yang bagus",
                "dengan warna kulit cerah, kombinasikan blazer gelap dengan kemeja pastel dan celana bahan",
                "untuk tone kulit cerah, padukan kemeja lengan panjang warna pastel dengan celana bahan gelap",
            ],
            "formal_pria_dark": [
                "untuk pria berkulit sawo matang, kenakan setelan jas berwarna earth tone dengan kemeja putih",
                "dengan warna kulit sawo matang, kombinasikan blazer coklat tua dengan kemeja cream",
                "untuk tone kulit gelap, padukan kemeja warna jewel tone dengan celana bahan hitam",
            ],
            "formal_wanita_light": [
                "untuk wanita berkulit cerah, kenakan blazer navy dengan rok pensil dan blus pastel",
                "dengan warna kulit cerah, padukan dress formal warna nude dengan blazer gelap",
                "untuk tone kulit cerah, gunakan setelan formal warna pastel dengan aksen gelap",
            ],
            "formal_wanita_dark": [
                "untuk wanita berkulit sawo matang, kenakan blazer hitam atau coklat tua dengan dress warna earth tone",
                "dengan warna kulit sawo matang, padukan blus berwarna jewel tone dengan rok pensil hitam",
                "untuk tone kulit gelap, gunakan kombinasi warna deep burgundy atau navy",
            ],
            "kasual_pria_light": [
                "untuk pria berkulit cerah, kenakan kaos putih atau pastel dengan jeans biru",
                "dengan warna kulit cerah, padukan polo shirt warna muted dengan chinos",
                "untuk tone kulit cerah, gunakan kemeja casual motif dengan celana chino warna neutral",
            ],
            "kasual_pria_dark": [
                "untuk pria berkulit sawo matang, kenakan kaos dengan warna-warna cerah",
                "dengan warna kulit sawo matang, padukan kemeja casual bermotif dengan jeans gelap",
                "untuk tone kulit gelap, gunakan polo shirt warna jewel tone dengan celana chino",
            ],
            "kasual_wanita_light": [
                "untuk wanita berkulit cerah, kenakan dress casual warna pastel",
                "dengan warna kulit cerah, padukan kaos neutral dengan rok atau celana warna cerah",
                "untuk tone kulit cerah, gunakan blus pastel dengan jeans",
            ],
            "kasual_wanita_dark": [
                "untuk wanita berkulit sawo matang, kenakan dress dengan warna-warna bold",
                "dengan warna kulit sawo matang, padukan atasan warna jewel tone dengan jeans",
                "untuk tone kulit gelap, gunakan blus bermotif dengan celana atau rok polos",
            ],
            "wedding": [
                "kenakan gaun panjang dengan heels dan clutch bag",
                "padukan kebaya modern dengan rok panjang dan selop",
                "gunakan dress formal dengan warna pastel dan sepatu hak tinggi",
            ],
            "party": [
                "kenakan dress party dengan aksesoris berkilau",
                "padukan kemeja fancy dengan celana formal",
                "kombinasikan blus berkilau dengan rok atau celana hitam",
            ],
            "hot_weather": [
                "kenakan pakaian berbahan katun yang menyerap keringat",
                "padukan kaos lengan pendek dengan celana pendek",
                "gunakan baju berbahan ringan dan breathable",
            ],
            "cold_weather": [
                "kenakan sweater tebal dengan celana panjang",
                "padukan jaket tebal dengan syal dan boots",
                "gunakan pakaian berlapis dengan mantel hangat",
            ],
            "rainy_weather": [
                "kenakan jas hujan dengan sepatu anti air",
                "padukan jaket waterproof dengan celana panjang dan boots",
                "gunakan pakaian yang cepat kering dengan sepatu boots anti air",
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
        return 1

    def generate_response(self, text, intent, sentiment):
        """Generate contextual response based on intent and sentiment"""
        try:
            print(f"Generating response for intent: {intent}")

            if intent in self.responses:
                return np.random.choice(self.responses[intent])

            # Default response if no specific response is found
            return "Maaf, bisakah Anda menjelaskan lebih detail tentang jenis pakaian yang Anda cari?"

        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "Maaf, bisakah Anda mengulangi pertanyaan Anda?"
