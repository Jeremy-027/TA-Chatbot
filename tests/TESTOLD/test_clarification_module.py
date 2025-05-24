# tests/test_clarification_module.py
import unittest
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from clarification_module import ClarificationModule


class TestClarificationModule(unittest.TestCase):
    def setUp(self):
        """Set up the ClarificationModule for testing"""
        self.clarification = ClarificationModule()

    def test_gender_keyword_extraction(self):
        """Test that gender keywords are correctly extracted"""
        # Test male keywords
        male_texts = [
            "Pakaian untuk pria ke kantor",
            "Outfit cowok untuk santai",
            "Rekomendasi baju buat laki-laki",
            "Bapak mau ke pesta",
            "Mas perlu baju kerja",
        ]

        for text in male_texts:
            params = self.clarification.extract_parameters(text)
            self.assertEqual(
                params["gender"], "pria", f"Failed to extract male gender from: {text}"
            )

        # Test female keywords
        female_texts = [
            "Pakaian untuk wanita ke kantor",
            "Outfit cewek untuk santai",
            "Rekomendasi baju buat perempuan",
            "Ibu mau ke pesta",
            "Mbak perlu baju kerja",
        ]

        for text in female_texts:
            params = self.clarification.extract_parameters(text)
            self.assertEqual(
                params["gender"],
                "wanita",
                f"Failed to extract female gender from: {text}",
            )

    def test_skin_tone_extraction(self):
        """Test that skin tone keywords are correctly extracted"""
        # Light skin tones
        light_texts = [
            "Outfit untuk kulit cerah",
            "Pakaian untuk kulit putih",
            "Baju untuk kulit kuning langsat",
        ]

        for text in light_texts:
            params = self.clarification.extract_parameters(text)
            self.assertEqual(
                params["skin_tone"],
                "light",
                f"Failed to extract light skin tone from: {text}",
            )

        # Dark skin tones
        dark_texts = [
            "Outfit untuk kulit sawo matang",
            "Pakaian untuk kulit gelap",
            "Baju untuk kulit coklat",
        ]

        for text in dark_texts:
            params = self.clarification.extract_parameters(text)
            self.assertEqual(
                params["skin_tone"],
                "dark",
                f"Failed to extract dark skin tone from: {text}",
            )

    def test_occasion_extraction(self):
        """Test that occasion keywords are correctly extracted"""
        # Formal occasions
        formal_texts = [
            "Baju untuk formal",
            "Pakaian untuk kerja",
            "Outfit untuk interview",
            "Baju untuk ke kantor",
            "Pakaian untuk meeting",
        ]

        for text in formal_texts:
            params = self.clarification.extract_parameters(text)
            self.assertEqual(
                params["occasion"],
                "formal",
                f"Failed to extract formal occasion from: {text}",
            )

        # Casual occasions
        casual_texts = [
            "Baju untuk santai",
            "Pakaian untuk casual",
            "Outfit untuk jalan-jalan",
            "Baju untuk hangout",
            "Pakaian untuk main",
        ]

        for text in casual_texts:
            params = self.clarification.extract_parameters(text)
            self.assertEqual(
                params["occasion"],
                "casual",
                f"Failed to extract casual occasion from: {text}",
            )

        # Special case - interview should be detected as "interview" specifically
        interview_text = "Baju untuk interview pekerjaan"
        params = self.clarification.extract_parameters(interview_text)
        self.assertEqual(
            params["occasion"],
            "interview",
            "Failed to extract 'interview' as specific occasion",
        )

    def test_complex_parameter_extraction(self):
        """Test extraction of multiple parameters from complex queries"""
        complex_queries = [
            {
                "text": "Saya pria berkulit sawo matang mencari pakaian untuk interview",
                "expected": {
                    "gender": "pria",
                    "skin_tone": "dark",
                    "occasion": "interview",
                },
            },
            {
                "text": "Rekomendasi outfit casual untuk wanita kulit cerah",
                "expected": {
                    "gender": "wanita",
                    "skin_tone": "light",
                    "occasion": "casual",
                },
            },
            {
                "text": "Baju formal cowok putih",
                "expected": {
                    "gender": "pria",
                    "skin_tone": "light",
                    "occasion": "formal",
                },
            },
            {
                "text": "Pakaian untuk mbak berkulit coklat ke kantor",
                "expected": {
                    "gender": "wanita",
                    "skin_tone": "dark",
                    "occasion": "formal",
                },
            },
        ]

        for query in complex_queries:
            params = self.clarification.extract_parameters(query["text"])
            for key, expected_value in query["expected"].items():
                self.assertEqual(
                    params[key],
                    expected_value,
                    f"Failed to extract {key}='{expected_value}' from: {query['text']}",
                )

    def test_clarification_questions(self):
        """Test that appropriate clarification questions are generated for missing parameters"""
        # Missing gender
        params = {"gender": None, "skin_tone": "light", "occasion": "formal"}
        question = self.clarification.get_clarification_question(params)
        self.assertIsNotNone(question)
        self.assertIn("pria atau wanita", question.lower())

        # Missing skin tone
        params = {"gender": "pria", "skin_tone": None, "occasion": "formal"}
        question = self.clarification.get_clarification_question(params)
        self.assertIsNotNone(question)
        self.assertIn("warna kulit", question.lower())

        # Missing occasion
        params = {"gender": "pria", "skin_tone": "light", "occasion": None}
        question = self.clarification.get_clarification_question(params)
        self.assertIsNotNone(question)
        self.assertIn("acara", question.lower())

        # All parameters present
        params = {"gender": "pria", "skin_tone": "light", "occasion": "formal"}
        question = self.clarification.get_clarification_question(params)
        self.assertIsNone(question)

    def test_empty_input(self):
        """Test behavior with empty input"""
        params = self.clarification.extract_parameters("")
        self.assertIsNone(params["gender"])
        self.assertIsNone(params["skin_tone"])
        self.assertIsNone(params["occasion"])


if __name__ == "__main__":
    unittest.main()
