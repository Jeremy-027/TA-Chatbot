# src/clothing_selector.py
import json
import re
from fashion_mapping import FashionMapping, fashion_mapping

# Create an instance of FashionMapping
fashion_mapping_instance = FashionMapping()


def generate_clothing_selection(parameters):
    """
    Process parameters and generate clothing selection for 3D visualization

    Args:
        parameters (dict): Contains gender, skin_tone, occasion, weather, season

    Returns:
        str: JSON-formatted string with clothing selections
    """
    try:
        gender = parameters.get("gender", "neutral")
        skin_tone = parameters.get("skin_tone", "neutral")
        occasion = parameters.get("occasion", "casual")
        weather = parameters.get("weather", None)
        season = parameters.get("season", None)

        # Get appropriate clothing from the mapping
        if occasion in fashion_mapping["occasion_mappings"]:
            clothing_options = fashion_mapping["occasion_mappings"][occasion]

            # Get skin tone specific options
            if skin_tone in clothing_options:
                skin_tone_options = clothing_options[skin_tone]
            else:
                # Default to light if skin tone not found
                skin_tone_options = clothing_options.get("light", {})

            # Get gender specific options
            if gender in skin_tone_options:
                gender_options = skin_tone_options[gender]
            else:
                # Default to first available gender if not found
                gender_options = (
                    next(iter(skin_tone_options.values())) if skin_tone_options else {}
                )

            # Select random items from each category
            import random

            result = {
                "parameters": {
                    "gender": gender,
                    "skin_tone": skin_tone,
                    "occasion": occasion,
                    "weather": weather,
                    "season": season,
                },
                "clothing": {
                    "top": random.choice(gender_options.get("tops", ["baju"])),
                    "bottom": random.choice(gender_options.get("bottoms", ["celana"])),
                    "shoes": random.choice(gender_options.get("shoes", ["sepatu"])),
                    "accessory": random.choice(
                        gender_options.get("accessories", ["aksesoris"])
                    ),
                    "color_main": random.choice(
                        gender_options.get("colors_best", ["biru"])
                    ),
                },
            }

            # Add weather specific items if available
            if weather and weather in fashion_mapping["weather_mappings"]:
                weather_options = fashion_mapping["weather_mappings"][weather]
                result["weather"] = {
                    "material": random.choice(
                        weather_options.get("materials", ["katun"])
                    ),
                    "style": random.choice(weather_options.get("styles", ["biasa"])),
                }

            # Add seasonal items if available
            if season and season in fashion_mapping["seasonal_mappings"]:
                season_options = fashion_mapping["seasonal_mappings"][season]
                result["season"] = {
                    "color": random.choice(season_options.get("colors", ["biru"])),
                    "pattern": random.choice(season_options.get("patterns", ["polos"])),
                    "material": random.choice(
                        season_options.get("materials", ["katun"])
                    ),
                }

            # Convert to JSON string
            return json.dumps(result, indent=2)
        else:
            # Default response if occasion not found
            return json.dumps(
                {
                    "parameters": {
                        "gender": gender,
                        "skin_tone": skin_tone,
                        "occasion": "casual",
                        "weather": weather,
                        "season": season,
                    },
                    "clothing": {
                        "top": "kemeja casual",
                        "bottom": "celana jeans",
                        "shoes": "sepatu sneakers",
                        "accessory": "jam tangan",
                        "color_main": "navy blue",
                    },
                },
                indent=2,
            )

    except Exception as e:
        # Fallback in case of error
        return json.dumps({"error": str(e), "parameters": parameters}, indent=2)
