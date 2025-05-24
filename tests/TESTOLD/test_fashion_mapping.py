# tests/test_fashion_mapping.py
import unittest
import sys
import os
import json

# Add the src directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from fashion_mapping import FashionMapping


class TestFashionMapping(unittest.TestCase):
    def setUp(self):
        """Set up FashionMapping for testing"""
        self.fashion_mapping = FashionMapping()

    def test_mapping_initialization(self):
        """Test that the fashion mapping is correctly initialized"""
        # Verify structure exists
        self.assertIsNotNone(self.fashion_mapping.fashion_mapping)

        # Check main categories exist
        self.assertIn("occasion_mappings", self.fashion_mapping.fashion_mapping)
        self.assertIn("weather_mappings", self.fashion_mapping.fashion_mapping)
        self.assertIn("seasonal_mappings", self.fashion_mapping.fashion_mapping)

        # Check occasion categories exist
        occasion_mappings = self.fashion_mapping.fashion_mapping["occasion_mappings"]
        self.assertIn("formal", occasion_mappings)
        self.assertIn("casual", occasion_mappings)

        # Check skin tones exist
        self.assertIn("light", occasion_mappings["formal"])
        self.assertIn("dark", occasion_mappings["formal"])

        # Check gender categories exist
        self.assertIn("pria", occasion_mappings["formal"]["light"])
        self.assertIn("wanita", occasion_mappings["formal"]["light"])

    def test_get_recommendation_formal_pria_light(self):
        """Test recommendations for formal men's wear with light skin tone"""
        parameters = {"gender": "pria", "skin_tone": "light", "occasion": "formal"}

        recommendation = self.fashion_mapping.get_recommendation(parameters)

        # Check that recommendation has expected keys
        self.assertIn("tops", recommendation)
        self.assertIn("bottoms", recommendation)
        self.assertIn("shoes", recommendation)
        self.assertIn("accessories", recommendation)
        self.assertIn("colors_best", recommendation)

        # Verify some expected formal male clothing items are included
        tops = recommendation["tops"]
        self.assertTrue(
            any("jas" in item.lower() or "blazer" in item.lower() for item in tops),
            "Formal men's tops should include suit/blazer options",
        )

    def test_get_recommendation_casual_wanita_dark(self):
        """Test recommendations for casual women's wear with dark skin tone"""
        parameters = {"gender": "wanita", "skin_tone": "dark", "occasion": "casual"}

        recommendation = self.fashion_mapping.get_recommendation(parameters)

        # Check casual women's clothing recommendations
        self.assertIn("tops", recommendation)
        self.assertIn("bottoms", recommendation)

        # Verify expected casual female clothing items
        tops = recommendation["tops"]
        bottoms = recommendation["bottoms"]

        casual_top_keywords = ["blus", "t-shirt", "crop", "kaos"]
        casual_bottom_keywords = ["jeans", "rok", "leggings", "shorts"]

        self.assertTrue(
            any(keyword in " ".join(tops).lower() for keyword in casual_top_keywords),
            f"Casual women's tops should include some of: {casual_top_keywords}",
        )

        self.assertTrue(
            any(
                keyword in " ".join(bottoms).lower()
                for keyword in casual_bottom_keywords
            ),
            f"Casual women's bottoms should include some of: {casual_bottom_keywords}",
        )

    def test_weather_recommendations(self):
        """Test weather-specific clothing recommendations"""
        # Hot weather
        hot_params = {
            "gender": "pria",
            "skin_tone": "light",
            "occasion": "casual",
            "weather": "hot_weather",
        }

        hot_recommendation = self.fashion_mapping.get_recommendation(hot_params)

        # Check hot weather additions
        self.assertIn("weather_tips", hot_recommendation)
        self.assertIn("materials", hot_recommendation)
        self.assertIn("styles", hot_recommendation)

        # Verify appropriate materials for hot weather
        hot_materials = hot_recommendation["materials"]
        cool_material_keywords = ["katun", "linen", "breathable", "ringan"]
        self.assertTrue(
            any(material in cool_material_keywords for material in hot_materials),
            "Hot weather materials should include breathable options",
        )

        # Cold weather
        cold_params = {
            "gender": "wanita",
            "skin_tone": "dark",
            "occasion": "formal",
            "weather": "cold_weather",
        }

        cold_recommendation = self.fashion_mapping.get_recommendation(cold_params)

        # Verify appropriate materials for cold weather
        cold_materials = cold_recommendation["materials"]
        warm_material_keywords = ["wool", "fleece", "tebal"]
        self.assertTrue(
            any(material in warm_material_keywords for material in cold_materials),
            "Cold weather materials should include warm options",
        )

    def test_seasonal_recommendations(self):
        """Test seasonal clothing recommendations"""
        # Summer season
        summer_params = {
            "gender": "pria",
            "skin_tone": "light",
            "occasion": "casual",
            "season": "summer",
        }

        summer_recommendation = self.fashion_mapping.get_recommendation(summer_params)

        # Check summer additions
        self.assertIn("seasonal_colors", summer_recommendation)
        self.assertIn("seasonal_patterns", summer_recommendation)
        self.assertIn("seasonal_tips", summer_recommendation)

        # Verify summer colors
        summer_colors = summer_recommendation["seasonal_colors"]
        bright_colors = ["white", "blue", "coral", "yellow", "turquoise"]
        self.assertTrue(
            any(
                color.lower() in " ".join(summer_colors).lower()
                for color in bright_colors
            ),
            "Summer colors should include bright options",
        )

        # Winter season
        winter_params = {
            "gender": "wanita",
            "skin_tone": "dark",
            "occasion": "formal",
            "season": "winter",
        }

        winter_recommendation = self.fashion_mapping.get_recommendation(winter_params)

        # Verify winter colors and patterns
        winter_colors = winter_recommendation["seasonal_colors"]
        winter_patterns = winter_recommendation["seasonal_patterns"]

        dark_colors = ["red", "green", "navy", "charcoal", "black"]
        winter_pattern_types = ["fair isle", "tartan", "solid", "geometric"]

        self.assertTrue(
            any(
                color.lower() in " ".join(winter_colors).lower()
                for color in dark_colors
            ),
            "Winter colors should include dark/rich options",
        )

        self.assertTrue(
            any(
                pattern.lower() in " ".join(winter_patterns).lower()
                for pattern in winter_pattern_types
            ),
            "Winter patterns should include appropriate options",
        )

    def test_format_recommendation(self):
        """Test the natural language formatting of recommendations"""
        parameters = {"gender": "pria", "skin_tone": "light", "occasion": "formal"}

        recommendation = self.fashion_mapping.get_recommendation(parameters)
        formatted_text = self.fashion_mapping.format_recommendation(
            recommendation, parameters
        )

        # Check that the formatted text mentions key elements
        self.assertIn("pria", formatted_text.lower())
        self.assertIn("kulit", formatted_text.lower())
        self.assertIn("formal", formatted_text.lower())

        # Should include clothing items
        has_clothing_item = False
        clothing_keywords = ["jas", "kemeja", "celana", "sepatu", "blazer"]
        for keyword in clothing_keywords:
            if keyword in formatted_text.lower():
                has_clothing_item = True
                break

        self.assertTrue(
            has_clothing_item, "Formatted recommendation should include clothing items"
        )

        # Should include color recommendations
        self.assertTrue(
            "warna" in formatted_text.lower(),
            "Formatted recommendation should include color advice",
        )

    def test_default_parameters(self):
        """Test behavior with missing parameters using defaults"""
        # Missing gender
        parameters_missing_gender = {"skin_tone": "light", "occasion": "formal"}

        recommendation = self.fashion_mapping.get_recommendation(
            parameters_missing_gender
        )
        # Should default to male
        self.assertIsNotNone(recommendation)

        # Missing skin tone
        parameters_missing_skin = {"gender": "wanita", "occasion": "casual"}

        recommendation = self.fashion_mapping.get_recommendation(
            parameters_missing_skin
        )
        # Should default to light
        self.assertIsNotNone(recommendation)

        # Missing occasion
        parameters_missing_occasion = {"gender": "pria", "skin_tone": "dark"}

        recommendation = self.fashion_mapping.get_recommendation(
            parameters_missing_occasion
        )
        # Should default to casual
        self.assertIsNotNone(recommendation)

        # All parameters missing
        empty_parameters = {}
        recommendation = self.fashion_mapping.get_recommendation(empty_parameters)
        # Should provide some default recommendation
        self.assertIsNotNone(recommendation)


if __name__ == "__main__":
    unittest.main()
