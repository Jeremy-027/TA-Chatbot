# src/clarification_module.py


class ClarificationModule:
    def __init__(self):
        self.skin_tone_keywords = {
            "very_light": ["sangat cerah", "putih pucat", "kulit putih"],
            "light": ["cerah", "putih", "kuning langsat"],
            "medium": ["sawo matang muda", "kuning kecoklatan", "tan"],
            "dark": ["sawo matang", "coklat", "gelap"],
            "very_dark": ["coklat tua", "hitam manis", "kulit gelap"],
        }

        self.gender_keywords = {
            "pria": ["pria", "laki-laki", "cowok", "mas", "bapak"],
            "wanita": ["wanita", "perempuan", "cewek", "mbak", "ibu"],
        }

        self.occasion_keywords = {
            "formal": ["formal", "kerja", "interview", "kantor", "meeting"],
            "casual": ["santai", "casual", "jalan-jalan", "hangout", "main"],
        }

    def extract_parameters(self, text: str) -> dict:
        """Extract gender, skin tone and occasion from text"""
        params = {"gender": None, "skin_tone": None, "occasion": None}

        # Extract gender
        for gender, keywords in self.gender_keywords.items():
            if any(keyword in text.lower() for keyword in keywords):
                params["gender"] = gender
                break

        # Extract skin tone
        for tone, keywords in self.skin_tone_keywords.items():
            if any(keyword in text.lower() for keyword in keywords):
                params["skin_tone"] = tone
                break

        # Extract occasion
        for occasion, keywords in self.occasion_keywords.items():
            if any(keyword in text.lower() for keyword in keywords):
                params["occasion"] = occasion
                # Additional parsing for specific occasions
                if "interview" in text.lower():
                    params["occasion"] = "interview"
                break

        return params

    def get_clarification_question(self, params: dict) -> str:
        """Get appropriate clarification question for missing parameters"""
        if params["gender"] is None:
            return "Apakah rekomendasi ini untuk pria atau wanita?"

        if params["skin_tone"] is None:
            return "Bagaimana warna kulit Anda? (cerah, sawo matang, atau gelap?)"

        if params["occasion"] is None:
            return "Untuk acara apa pakaian ini akan dikenakan? (formal, casual, atau acara khusus?)"

        return None
