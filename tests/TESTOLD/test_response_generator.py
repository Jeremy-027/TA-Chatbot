# tests/test_response_generator.py
import unittest
import sys
import os
import json
import re

# Add the src directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from response_generator import ResponseGenerator


class TestResponseGenerator(unittest.TestCase):
    def setUp(self):
        """Set up ResponseGenerator for testing"""
        self.response_generator = ResponseGenerator()

    def test_initialization(self):
        """Test that ResponseGenerator initializes correctly with all required data"""
        # Check clothing items are loaded
        self.assertIn("formal_pria", self.response_generator.clothing_items)
        self.assertIn("formal_wanita", self.response_generator.clothing_items)
        self.assertIn("casual_pria", self.response_generator.clothing_items)
        self.assertIn("casual_wanita", self.response_generator.clothing_items)

        # Check color palettes
        self.assertIn("light", self.response_generator.color_palettes)
        self.assertIn("dark", self.response_generator.color_palettes)

        # Check weather modifiers
        self.assertIn("hot", self.response_generator.weather_modifiers)
        self.assertIn("cold", self.response_generator.weather_modifiers)
        self.assertIn("rainy", self.response_generator.weather_modifiers)
        self.assertIn("windy", self.response_generator.weather_modifiers)

        # Check response templates
        self.assertTrue(len(self.response_generator.templates) > 0)
        self.assertIn("occasion_templates", self.response_generator.occasion_templates)

    def test_determine_style(self):
        """Test the style determination based on occasion"""
        # Formal occasions
        formal_occasions = [
            "formal",
            "kerja",
            "interview",
            "meeting",
            "rapat",
            "kantor",
        ]
        for occasion in formal_occasions:
            style = self.response_generator._determine_style(occasion)
            self.assertEqual(
                style, "formal", f"Occasion '{occasion}' should be determined as formal"
            )

        # Weather occasions
        weather_occasions = ["panas", "dingin", "hujan", "berangin"]
        for occasion in weather_occasions:
            style = self.response_generator._determine_style(occasion)
            self.assertEqual(
                style,
                "weather",
                f"Occasion '{occasion}' should be determined as weather",
            )

        # Casual occasions (default)
        casual_occasions = ["casual", "santai", "jalan-jalan", "hangout", "party"]
        for occasion in casual_occasions:
            style = self.response_generator._determine_style(occasion)
            self.assertEqual(
                style, "casual", f"Occasion '{occasion}' should be determined as casual"
            )

    def test_get_clothing_items(self):
        """Test getting clothing items based on gender and style"""
        # Test formal male
        formal_male_items = self.response_generator._get_clothing_items("formal_pria")
        self.assertIn("top", formal_male_items)
        self.assertIn("bottom", formal_male_items)
        self.assertIn("shoes", formal_male_items)
        self.assertIn("accessory", formal_male_items)

        # Test casual female
        casual_female_items = self.response_generator._get_clothing_items(
            "casual_wanita"
        )
        self.assertIn("top", casual_female_items)
        self.assertIn("bottom", casual_female_items)
        self.assertIn("shoes", casual_female_items)
        self.assertIn("accessory", casual_female_items)

        # Test invalid style (should default to casual_pria)
        invalid_items = self.response_generator._get_clothing_items("invalid_style")
        self.assertIn("top", invalid_items)
        self.assertIn("bottom", invalid_items)
        self.assertIn("shoes", invalid_items)
        self.assertIn("accessory", invalid_items)

    def test_get_colors(self):
        """Test getting color recommendations based on skin tone and style"""
        # Test light skin with formal style
        light_formal_colors = self.response_generator._get_colors("light", "formal")
        self.assertIn("main", light_formal_colors)
        self.assertIn("accent", light_formal_colors)

        # Make sure main color is from formal palette
        light_formal_palette = self.response_generator.color_palettes["light"]["formal"]
        self.assertIn(light_formal_colors["main"], light_formal_palette)

        # Test dark skin with casual style
        dark_casual_colors = self.response_generator._get_colors("dark", "casual")
        self.assertIn("main", dark_casual_colors)
        self.assertIn("accent", dark_casual_colors)

        # Make sure main color is from casual palette
        dark_casual_palette = self.response_generator.color_palettes["dark"]["casual"]
        self.assertIn(dark_casual_colors["main"], dark_casual_palette)

        # Test extended skin tones (should map to light/dark)
        very_light_colors = self.response_generator._get_colors("very_light", "casual")
        self.assertIn("main", very_light_colors)
        self.assertIn("accent", very_light_colors)

        # Test invalid skin tone (should default to medium -> light)
        invalid_colors = self.response_generator._get_colors("invalid_tone", "formal")
        self.assertIn("main", invalid_colors)
        self.assertIn("accent", invalid_colors)

    def test_modify_for_weather(self):
        """Test weather-specific modifications to clothing recommendations"""
        items = {
            "top": "kemeja",
            "bottom": "celana bahan",
            "shoes": "sepatu formal",
            "accessory": "dasi",
        }

        # Test hot weather modifications
        hot_items = self.response_generator._modify_for_weather(items.copy(), "hot")
        self.assertIn("material", hot_items)
        self.assertIn(
            hot_items["material"],
            self.response_generator.weather_modifiers["hot"]["materials"],
        )
        self.assertTrue(
            "berbahan" in hot_items["top"], "Hot weather top should mention material"
        )

        # Test cold weather modifications
        cold_items = self.response_generator._modify_for_weather(items.copy(), "cold")
        self.assertIn("material", cold_items)
        self.assertIn(
            cold_items["material"],
            self.response_generator.weather_modifiers["cold"]["materials"],
        )
        self.assertTrue(
            "berbahan" in cold_items["top"], "Cold weather top should mention material"
        )

        # Test rainy weather modifications
        rainy_items = self.response_generator._modify_for_weather(items.copy(), "rainy")
        self.assertIn("material", rainy_items)
        self.assertIn(
            rainy_items["material"],
            self.response_generator.weather_modifiers["rainy"]["materials"],
        )

        # Test invalid weather (should return original items)
        invalid_weather_items = self.response_generator._modify_for_weather(
            items.copy(), "invalid_weather"
        )
        self.assertEqual(items, invalid_weather_items)

    def test_format_response(self):
        """Test formatting the final natural language response"""
        items = {
            "top": "kemeja formal",
            "bottom": "celana bahan",
            "shoes": "sepatu oxford",
            "accessory": "dasi slim",
            "material": "katun",
        }

        colors = {"main": "navy blue", "accent": "burgundy"}

        parameters = {"gender": "pria", "skin_tone": "light", "occasion": "interview"}

        response = self.response_generator._format_response(items, colors, parameters)

        # Response should include key elements
        self.assertIn("interview", response.lower())
        self.assertIn("pria", response.lower())
        self.assertIn("kemeja", response.lower())
        self.assertIn("navy blue", response.lower())

        # Test different occasion type
        parameters["occasion"] = "casual hangout"
        response = self.response_generator._format_response(items, colors, parameters)
        self.assertIn("casual", response.lower())

        # Test weather occasion
        parameters["occasion"] = "cuaca panas"
        items["material"] = "linen"
        response = self.response_generator._format_response(items, colors, parameters)
        self.assertIn("linen", response.lower())

    def test_generate_response(self):
        """Test the complete response generation flow"""
        # Test formal male recommendation
        formal_male_params = {
            "gender": "pria",
            "skin_tone": "light",
            "occasion": "formal",
        }

        response_text, clothing_json = self.response_generator.generate_response(
            formal_male_params
        )

        # Check text response
        self.assertIsNotNone(response_text)
        self.assertTrue(len(response_text) > 0)

        # Text should include key parameters
        self.assertIn("pria", response_text.lower())
        self.assertIn("formal", response_text.lower())

        # Check JSON output
        self.assertIsNotNone(clothing_json)
        clothing_data = json.loads(clothing_json)

        # JSON should have correct structure
        self.assertIn("parameters", clothing_data)
        self.assertIn("clothing", clothing_data)
        self.assertEqual(clothing_data["parameters"]["gender"], "pria")
        self.assertEqual(clothing_data["parameters"]["skin_tone"], "light")
        self.assertEqual(clothing_data["parameters"]["occasion"], "formal")

        # Test casual female with weather
        casual_female_params = {
            "gender": "wanita",
            "skin_tone": "dark",
            "occasion": "casual",
            "weather": "hot",
        }

        response_text, clothing_json = self.response_generator.generate_response(
            casual_female_params
        )

        # Check text response
        self.assertIsNotNone(response_text)
        self.assertTrue(len(response_text) > 0)

        # Text should include key parameters
        self.assertIn("wanita", response_text.lower())
        self.assertIn("casual", response_text.lower())

        # Check if response contains weather-specific advice
        weather_materials = self.response_generator.weather_modifiers["hot"][
            "materials"
        ]
        has_weather_material = False
        for material in weather_materials:
            if material in response_text.lower():
                has_weather_material = True
                break

        self.assertTrue(
            has_weather_material,
            "Response should include weather-appropriate materials",
        )

        # Check JSON output
        clothing_data = json.loads(clothing_json)
        self.assertEqual(clothing_data["parameters"]["gender"], "wanita")
        self.assertEqual(clothing_data["parameters"]["skin_tone"], "dark")
        self.assertEqual(clothing_data["parameters"]["occasion"], "casual")
        self.assertEqual(clothing_data["parameters"]["weather"], "hot")

    def test_empty_parameters(self):
        """Test response generation with empty parameters"""
        empty_params = {}

        response_text, clothing_json = self.response_generator.generate_response(
            empty_params
        )

        # Should still get a valid response
        self.assertIsNotNone(response_text)
        self.assertTrue(len(response_text) > 0)

        # Should get valid JSON
        clothing_data = json.loads(clothing_json)
        self.assertIn("parameters", clothing_data)
        self.assertIn("clothing", clothing_data)


if __name__ == "__main__":
    unittest.main()
