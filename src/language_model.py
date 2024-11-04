# src/language_model.py
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForCausalLM
import numpy as np

class IndoBERTProcessor:
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
            19: "other"
        }

        # Load sentiment analysis model
        self.sentiment_tokenizer = AutoTokenizer.from_pretrained("indobert-base-p2")
        self.sentiment_model = AutoModelForSequenceClassification.from_pretrained("indobert-base-p2")
        self.sentiment_model.to(self.device)

    def preprocess_text(self, text):
        """Preprocess text for IndoBERT"""
        # Tokenize the text
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=128,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )

        return encoding.to(self.device)

    def classify_intent(self, text):
        """Classify user intent using IndoBERT"""
        inputs = self.preprocess_text(text)
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.softmax(outputs.logits, dim=1)
            category_id = torch.argmax(predictions, dim=1).item()
        return self.categories.get(category_id, "other")

    def analyze_sentiment(self, text):
        """Analyze sentiment of user input"""
        inputs = self.sentiment_tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=128
        ).to(self.device)

        with torch.no_grad():
            outputs = self.sentiment_model(**inputs)
            sentiment_scores = torch.softmax(outputs.logits, dim=1)
            sentiment = torch.argmax(sentiment_scores, dim=1).item()

        return sentiment

    def generate_response(self, text, intent, sentiment):
        """Generate contextual response based on intent and sentiment"""
        responses = {
            "formal_pria": {
                "positive": ["Bagus sekali! Untuk acara formal, saya rekomendasikan setelan jas navy blue dengan kemeja putih."],
                "neutral": ["Untuk acara formal, Anda bisa mengenakan kemeja lengan panjang dengan celana bahan."],
                "negative": ["Jangan khawatir, saya akan membantu Anda memilih pakaian formal yang nyaman."]
            },
            "formal_wanita": {
                "positive": ["Excellent! Untuk acara formal, saya rekomendasikan blazer dengan rok pensil atau celana bahan."],
                "neutral": ["Untuk acara formal, Anda bisa mengenakan blus formal dengan rok atau celana bahan."],
                "negative": ["Jangan khawatir, kita akan temukan pakaian formal yang membuat Anda nyaman."]
            },
            "wedding": {
                "positive": ["Untuk pernikahan, saya sarankan dress formal dengan warna pastel dan sepatu hak tinggi."],
                "neutral": ["Setelan jas dengan dasi dan sepatu formal akan cocok untuk pernikahan."],
                "negative": ["Mari kita cari pakaian yang sesuai untuk pernikahan."]
            },
            "hot_weather": {
                "positive": ["Untuk cuaca panas, coba kenakan kaos katun dengan celana pendek dan sandal."],
                "neutral": ["Dress ringan dengan bahan yang menyerap keringat akan nyaman untuk cuaca panas."],
                "negative": ["Jangan khawatir, kita akan temukan pakaian yang nyaman untuk cuaca panas."]
            },
        }

        sentiment_map = {0: "negative", 1: "neutral", 2: "positive"}
        sentiment_label = sentiment_map[sentiment]

        if intent in responses:
            return np.random.choice(responses[intent][sentiment_label])
        else:
            return "Maaf, bisakah Anda menjelaskan lebih detail tentang jenis pakaian yang Anda cari?"


