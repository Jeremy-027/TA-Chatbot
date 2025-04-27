def generate_clothing_selection(user_input):
    """
    Process user input and generate clothing selection for 3D visualization

    Args:
        user_input (str): User's query about what to wear

    Returns:
        str: JSON-formatted string with clothing selections
    """
    import json
    import re

    # Extract parameters from user input
    gender = "neutral"
    skin_tone = "neutral"
    occasion = "casual"
    weather = None
    season = None

    # Gender detection
    if re.search(r"\b(pria|laki|cowok)\b", user_input.lower()):
        gender = "pria"
    elif re.search(r"\b(wanita|perempuan|cewek)\b", user_input.lower()):
        gender = "wanita"

    # Skin tone detection
    if re.search(r"\b(cerah|putih|kuning langsat)\b", user_input.lower()):
        skin_tone = "light"
    elif re.search(r"\b(sawo matang|gelap|coklat)\b", user_input.lower()):
        skin_tone = "dark"

    # Occasion detection
    if re.search(
        r"\b(formal|kerja|interview|meeting|rapat|kantor)\b", user_input.lower()
    ):
        occasion = "formal"
    elif re.search(r"\b(casual|santai|jalan|hangout|nongkrong)\b", user_input.lower()):
        occasion = "casual"
    elif re.search(r"\b(nikah|pernikahan|wedding)\b", user_input.lower()):
        occasion = "wedding"
    elif re.search(r"\b(pesta|party|ulang tahun)\b", user_input.lower()):
        occasion = "party"
    elif re.search(r"\b(bisnis|meeting|rapat)\b", user_input.lower()):
        occasion = "business_meeting"

    # Weather detection
    if re.search(r"\b(panas|terik|gerah)\b", user_input.lower()):
        weather = "hot_weather"
    elif re.search(r"\b(dingin|sejuk)\b", user_input.lower()):
        weather = "cold_weather"
    elif re.search(r"\b(hujan|gerimis)\b", user_input.lower()):
        weather = "rainy_weather"
    elif re.search(r"\b(angin|berangin)\b", user_input.lower()):
        weather = "windy_weather"

    # Season detection
    if re.search(r"\b(spring|semi)\b", user_input.lower()):
        season = "spring"
    elif re.search(r"\b(summer|panas|kemarau)\b", user_input.lower()):
        season = "summer"
    elif re.search(r"\b(autumn|gugur)\b", user_input.lower()):
        season = "autumn"
    elif re.search(r"\b(winter|dingin)\b", user_input.lower()):
        season = "winter"

    # Get appropriate clothing from the mapping
    try:
        # Get occasion mapping
        if occasion in fashion_mapping["occasion_mappings"]:
            clothing_options = fashion_mapping["occasion_mappings"][occasion]

            # Get skin tone specific options
            if skin_tone in clothing_options:
                skin_tone_options = clothing_options[skin_tone]
            else:
                # Default to light if skin tone not found
                skin_tone_options = clothing_options["light"]

            # Get gender specific options
            if gender in skin_tone_options:
                gender_options = skin_tone_options[gender]
            else:
                # Default to first available gender if not found
                gender_key = next(iter(skin_tone_options))
                gender_options = skin_tone_options[gender_key]

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
                    "top": (
                        random.choice(gender_options["tops"])
                        if "tops" in gender_options
                        else None
                    ),
                    "bottom": (
                        random.choice(gender_options["bottoms"])
                        if "bottoms" in gender_options
                        else None
                    ),
                    "shoes": (
                        random.choice(gender_options["shoes"])
                        if "shoes" in gender_options
                        else None
                    ),
                    "accessory": (
                        random.choice(gender_options["accessories"])
                        if "accessories" in gender_options
                        else None
                    ),
                    "color_main": (
                        random.choice(gender_options["colors_best"])
                        if "colors_best" in gender_options
                        else None
                    ),
                },
            }

            # Add weather specific items if available
            if weather and weather in fashion_mapping["weather_mappings"]:
                weather_options = fashion_mapping["weather_mappings"][weather]
                result["weather"] = {
                    "material": random.choice(weather_options["materials"]),
                    "style": random.choice(weather_options["styles"]),
                }

            # Add seasonal items if available
            if season and season in fashion_mapping["seasonal_mappings"]:
                season_options = fashion_mapping["seasonal_mappings"][season]
                result["season"] = {
                    "color": random.choice(season_options["colors"]),
                    "pattern": random.choice(season_options["patterns"]),
                    "material": random.choice(season_options["materials"]),
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
        return json.dumps(
            {
                "error": str(e),
                "parameters": {
                    "gender": gender,
                    "skin_tone": skin_tone,
                    "occasion": occasion,
                    "weather": weather,
                    "season": season,
                },
            },
            indent=2,
        )
