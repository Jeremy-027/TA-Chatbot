# tests/test_clothing_selector.py
import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add the src directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from clothing_selector import generate_clothing_selection


class TestClothingSelector(unittest.TestCase):
    def setUp(self):
        """Set up for clothing selector tests"""
        # Define some test parameters
        self.formal_male_params = {
            "gender": "pria",
            "skin_tone": "light",
            "occasion": "formal",
        }

        self.casual_female_params = {
            "gender": "wanita",
            "skin_tone": "dark",
            "occasion": "casual",
        }

        self.weather_params = {
            "gender": "pria",
            "skin_tone": "medium",
            "occasion": "casual",
            "weather": "hot",
        }

        self.seasonal_params = {
            "gender": "wanita",
            "skin_tone": "light",
            "occasion": "formal",
            "season": "winter",
        }

        self.complete_params = {
            "gender": "pria",
            "skin_tone": "dark",
            "occasion": "casual",
            "weather": "rainy",
            "season": "autumn",
        }

    def test_json_format(self):
        """Test that the output is valid JSON with the expected structure"""
        for params in [
            self.formal_male_params,
            self.casual_female_params,
            self.weather_params,
            self.seasonal_params,
            self.complete_params,
        ]:
            # Generate clothing selection
            result = generate_clothing_selection(params)

            # Verify it's a valid JSON string
            try:
                clothing_data = json.loads(result)
                self.assertIsInstance(clothing_data, dict)
            except json.JSONDecodeError:
                self.fail(
                    f"generate_clothing_selection did not return valid JSON: {result}"
                )

            # Check the basic structure
            self.assertIn("parameters", clothing_data)
            self.assertIn("clothing", clothing_data)

            # Parameters should reflect input
            for key, value in params.items():
                self.assertEqual(clothing_data["parameters"][key], value)

            # Clothing should have basic items
            self.assertIn("top", clothing_data["clothing"])
            self.assertIn("bottom", clothing_data["clothing"])
            self.assertIn("shoes", clothing_data["clothing"])
            self.assertIn("accessory", clothing_data["clothing"])
            self.assertIn("color_main", clothing_data["clothing"])

    def test_formal_male_clothing(self):
        """Test clothing selection for formal male occasion"""
        result = generate_clothing_selection(self.formal_male_params)
        clothing_data = json.loads(result)

        # Check that clothing items are appropriate for formal male
        top = clothing_data["clothing"]["top"].lower()
        bottom = clothing_data["clothing"]["bottom"].lower()
        shoes = clothing_data["clothing"]["shoes"].lower()

        formal_top_keywords = ["jas", "blazer", "kemeja"]
        formal_bottom_keywords = ["celana bahan", "celana formal", "celana wool"]
        formal_shoes_keywords = ["oxford", "pantofel", "loafers", "formal"]

        self.assertTrue(
            any(keyword in top for keyword in formal_top_keywords),
            f"Formal male top '{top}' should contain one of {formal_top_keywords}",
        )

        self.assertTrue(
            any(keyword in bottom for keyword in formal_bottom_keywords),
            f"Formal male bottom '{bottom}' should contain one of {formal_bottom_keywords}",
        )

        self.assertTrue(
            any(keyword in shoes for keyword in formal_shoes_keywords),
            f"Formal male shoes '{shoes}' should contain one of {formal_shoes_keywords}",
        )

    def test_casual_female_clothing(self):
        """Test clothing selection for casual female occasion"""
        result = generate_clothing_selection(self.casual_female_params)
        clothing_data = json.loads(result)

        # Check that clothing items are appropriate for casual female
        top = clothing_data["clothing"]["top"].lower()
        bottom = clothing_data["clothing"]["bottom"].lower()
        shoes = clothing_data["clothing"]["shoes"].lower()

        casual_top_keywords = ["blus", "t-shirt", "kaos", "crop", "kemeja casual"]
        casual_bottom_keywords = ["jeans", "rok", "shorts", "celana pendek", "leggings"]
        casual_shoes_keywords = ["sneakers", "flat", "sandal", "slip-on"]

        self.assertTrue(
            any(keyword in top for keyword in casual_top_keywords),
            f"Casual female top '{top}' should contain one of {casual_top_keywords}",
        )

        self.assertTrue(
            any(keyword in bottom for keyword in casual_bottom_keywords),
            f"Casual female bottom '{bottom}' should contain one of {casual_bottom_keywords}",
        )

        self.assertTrue(
            any(keyword in shoes for keyword in casual_shoes_keywords),
            f"Casual female shoes '{shoes}' should contain one of {casual_shoes_keywords}",
        )

    def test_weather_specific_clothing(self):
        """Test weather-specific clothing selection"""
        result = generate_clothing_selection(self.weather_params)
        clothing_data = json.loads(result)

        # Check for weather section
        self.assertIn("weather", clothing_data)
        self.assertIn("material", clothing_data["weather"])
        self.assertIn("style", clothing_data["weather"])

        # For hot weather, materials should be breathable
        hot_materials = ["katun", "linen", "breathable", "chambray", "seersucker"]
        material = clothing_data["weather"]["material"].lower()

        self.assertTrue(
            any(hot_mat in material for hot_mat in hot_materials),
            f"Hot weather material '{material}' should be one of {hot_materials}",
        )

        # Styles should be appropriate for hot weather
        hot_styles = ["loose-fit", "pendek", "flowy", "breathable", "ventilated"]
        style = clothing_data["weather"]["style"].lower()

        self.assertTrue(
            any(hot_style in style for hot_style in hot_styles),
            f"Hot weather style '{style}' should be one of {hot_styles}",
        )

    def test_seasonal_clothing(self):
        """Test seasonal clothing selection"""
        result = generate_clothing_selection(self.seasonal_params)
        clothing_data = json.loads(result)

        # Check for season section
        self.assertIn("season", clothing_data)
        self.assertIn("color", clothing_data["season"])
        self.assertIn("pattern", clothing_data["season"])
        self.assertIn("material", clothing_data["season"])

        # For winter, colors should be rich and dark
        winter_colors = [
            "deep",
            "rich",
            "dark",
            "emerald",
            "burgundy",
            "navy",
            "charcoal",
        ]
        color = clothing_data["season"]["color"].lower()

        # For winter, materials should be warm
        winter_materials = ["wool", "fleece", "cashmere", "heavy", "thick", "down"]
        material = clothing_data["season"]["material"].lower()

        self.assertTrue(
            any(winter_mat in material for winter_mat in winter_materials),
            f"Winter material '{material}' should contain one of {winter_materials}",
        )

    def test_complete_parameters(self):
        """Test clothing selection with all parameters specified"""
        result = generate_clothing_selection(self.complete_params)
        clothing_data = json.loads(result)

        # Check that all sections are present
        self.assertIn("parameters", clothing_data)
        self.assertIn("clothing", clothing_data)
        self.assertIn("weather", clothing_data)
        self.assertIn("season", clothing_data)

        # Verify parameters were correctly passed through
        params = clothing_data["parameters"]
        self.assertEqual(params["gender"], "pria")
        self.assertEqual(params["skin_tone"], "dark")
        self.assertEqual(params["occasion"], "casual")
        self.assertEqual(params["weather"], "rainy")
        self.assertEqual(params["season"], "autumn")

    def test_error_handling(self):
        """Test error handling in clothing selection"""
        # Test with invalid occasion
        invalid_params = {
            "gender": "pria",
            "skin_tone": "light",
            "occasion": "invalid_occasion",
        }

        result = generate_clothing_selection(invalid_params)
        clothing_data = json.loads(result)

        # Should default to casual
        self.assertEqual(clothing_data["parameters"]["occasion"], "invalid_occasion")
        self.assertIn("top", clothing_data["clothing"])

        # Test with missing gender
        missing_gender_params = {
            "skin_tone": "light",
            "occasion": "formal",
        }

        result = generate_clothing_selection(missing_gender_params)
        clothing_data = json.loads(result)

        # Should default to neutral gender
        self.assertEqual(clothing_data["parameters"]["gender"], "neutral")

        # Test with completely empty parameters
        empty_params = {}

        result = generate_clothing_selection(empty_params)
        clothing_data = json.loads(result)

        # Should provide defaults for all parameters
        self.assertIn("gender", clothing_data["parameters"])
        self.assertIn("skin_tone", clothing_data["parameters"])
        self.assertIn("occasion", clothing_data["parameters"])

        # Test with exception-triggering parameters
        with patch(
            "fashion_mapping.fashion_mapping", side_effect=Exception("Test error")
        ):
            result = generate_clothing_selection({"trigger_error": True})
            clothing_data = json.loads(result)

            # Should return error information
            self.assertIn("error", clothing_data)


if __name__ == "__main__":
    unittest.main()
