# src/response_generator.py
import random
from fashion_mapping import FashionMapping
from clothing_selector import generate_clothing_selection


class ResponseGenerator:
    def __init__(self):
        self.clothing_items = {
            "formal_pria": {
                "tops": ["jas", "blazer", "kemeja"],
                "bottoms": ["celana bahan", "celana formal", "celana panjang"],
                "shoes": ["sepatu pantofel", "sepatu formal", "oxford shoes"],
                "accessories": ["dasi", "jam tangan", "pocket square"],
            },
            "formal_wanita": {
                "tops": ["blazer", "blus", "kemeja wanita"],
                "bottoms": ["rok pensil", "celana bahan", "rok midi"],
                "shoes": ["high heels", "flat shoes", "wedges"],
                "accessories": ["tas formal", "anting minimalis", "kalung sederhana"],
            },
            "casual_pria": {
                "tops": ["kaos", "polo shirt", "kemeja casual"],
                "bottoms": ["jeans", "chino pants", "celana pendek"],
                "shoes": ["sneakers", "slip-on", "loafers"],
                "accessories": ["topi", "jam tangan casual", "gelang"],
            },
            "casual_wanita": {
                "tops": ["blus casual", "kaos", "t-shirt"],
                "bottoms": ["rok A-line", "jeans", "cullotes"],
                "shoes": ["flat shoes", "sneakers", "sandal"],
                "accessories": ["tas selempang", "gelang", "kalung casual"],
            },
        }

        self.weather_modifiers = {
            "hot": {
                "materials": ["katun", "linen", "breathable"],
                "styles": ["loose-fit", "sleeveless", "pendek"],
            },
            "cold": {
                "materials": ["wol", "fleece", "tebal"],
                "styles": ["berlapis", "lengan panjang", "tertutup"],
            },
            "rainy": {
                "materials": ["waterproof", "anti air", "quick dry"],
                "styles": ["tahan air", "tertutup", "berlapis"],
            },
            "windy": {
                "materials": ["windbreaker", "tahan angin", "denim"],
                "styles": ["pas badan", "tertutup", "berlapis"],
            },
        }

        self.color_palettes = {
            # Standard skin tones
            "light": {
                "formal": [
                    "navy blue",
                    "charcoal grey",
                    "deep burgundy",
                    "forest green",
                ],
                "casual": ["pastel blue", "mint green", "lavender", "light pink"],
                "accent": ["rose gold", "silver", "pearl white", "soft pink"],
            },
            "dark": {
                "formal": ["chocolate brown", "olive green", "deep gold", "terracotta"],
                "casual": ["bright yellow", "coral", "electric blue", "emerald green"],
                "accent": ["gold", "bronze", "copper", "bright red"],
            },
            # Extended skin tones
            "very_light": {
                "formal": ["navy", "burgundy", "forest green", "royal purple"],
                "casual": ["emerald", "deep teal", "ruby red", "sapphire blue"],
                "accent": ["coral", "deep pink", "gold", "turquoise"],
            },
            "medium": {
                "formal": ["deep teal", "aubergine", "olive green", "warm navy"],
                "casual": ["coral", "golden yellow", "jade green", "peacock blue"],
                "accent": ["gold", "copper", "turquoise", "bright orange"],
            },
            "very_dark": {
                "formal": ["white", "ivory", "bright red", "royal blue"],
                "casual": ["electric blue", "hot pink", "bright orange", "lime green"],
                "accent": ["silver", "gold", "fuchsia", "turquoise"],
            },
        }

        # Colors to avoid by skin tone (for more detailed recommendations)
        self.avoid_colors = {
            "very_light": ["neon yellow", "pale beige", "white", "pale pastels"],
            "light": ["orange-yellow", "bright orange", "beige"],
            "medium": ["browns similar to skin tone", "muted pastels"],
            "dark": ["dark brown", "navy", "muted earth tones"],
            "very_dark": ["black", "dark brown", "deep navy"],
        }

        self.templates = [
            "untuk {occasion}, {gender} berkulit {skin_tone} bisa mengenakan {top} warna {top_color} dengan {bottom} dan {shoes}",
            "kombinasikan {top} warna {top_color} dengan {bottom}, lengkapi dengan {shoes} dan {accessory}",
            "padukan {top} berwarna {top_color} dengan {bottom}, tambahkan {accessory} untuk melengkapi penampilan",
        ]

        # Adding more specific templates for different occasions
        self.occasion_templates = {
            "formal": [
                "untuk acara formal seperti {occasion}, {gender} berkulit {skin_tone} akan tampak profesional dengan {top} warna {top_color} dipadukan dengan {bottom} dan {shoes}",
                "tampil rapi di {occasion} dengan mengenakan {top} warna {top_color}, {bottom}, dan {shoes} yang elegan",
            ],
            "casual": [
                "untuk suasana santai seperti {occasion}, {gender} berkulit {skin_tone} bisa tampil stylish dengan {top} warna {top_color}, {bottom}, dan {shoes} yang nyaman",
                "tampil casual di {occasion} dengan mengenakan {top} warna {top_color} yang dipadukan dengan {bottom} dan {shoes}",
            ],
            "weather": [
                "untuk {occasion}, {gender} sebaiknya mengenakan {top} berbahan {material} dengan {bottom} dan {shoes} agar tetap nyaman",
                "hadapi {occasion} dengan nyaman menggunakan {top} warna {top_color} berbahan {material}, {bottom}, dan {shoes} yang sesuai",
            ],
        }

        self.fashion_mapping = FashionMapping()

    def generate_response(self, parameters):
        """
        Generate response based on extracted parameters
        parameters: dict containing gender, skin_tone, occasion, weather (optional)
        """
        gender = parameters.get("gender", "neutral")
        skin_tone = parameters.get("skin_tone", "neutral")
        occasion = parameters.get("occasion", "")
        weather = parameters.get("weather", None)

        recommendation = self.fashion_mapping.get_recommendation(parameters)
        clothing_json = generate_clothing_selection(text)
        # Determine style based on occasion
        style = self._determine_style(occasion)

        # Get base clothing items based on gender and style
        gender_style = (
            f"{style}_{gender}" if gender in ["pria", "wanita"] else f"{style}_pria"
        )
        items = self._get_clothing_items(gender_style)

        # Get colors based on skin tone
        colors = self._get_colors(skin_tone, style)

        # Apply weather modifications if applicable
        if weather in self.weather_modifiers:
            items = self._modify_for_weather(items, weather)

        # Generate response using templates
        response = self._format_response(items, colors, parameters)
        response = self.fashion_mapping.format_recommendation(
            recommendation, parameters
        )

        # Add skin tone specific color advice
        if skin_tone in self.avoid_colors:
            avoid = random.choice(self.avoid_colors[skin_tone])
            response += f" Hindari warna {avoid} karena kurang flattering untuk tone kulit Anda."

        return response, clothing_json

    def _determine_style(self, occasion):
        """Determine if occasion is formal or casual"""
        formal_keywords = [
            "formal",
            "kerja",
            "interview",
            "meeting",
            "rapat",
            "kantor",
            "bisnis",
            "presentasi",
        ]

        if any(keyword in occasion.lower() for keyword in formal_keywords):
            return "formal"

        # Check for weather-related occasions
        weather_keywords = ["panas", "dingin", "hujan", "berangin"]
        if any(keyword in occasion.lower() for keyword in weather_keywords):
            return "weather"

        return "casual"

    def _get_clothing_items(self, gender_style):
        """Get clothing items based on gender and style"""
        # Default to casual pria if not found
        if gender_style not in self.clothing_items:
            gender_style = "casual_pria"

        items = self.clothing_items[gender_style]

        return {
            "top": random.choice(items["tops"]),
            "bottom": random.choice(items["bottoms"]),
            "shoes": random.choice(items["shoes"]),
            "accessory": random.choice(items["accessories"]),
        }

    def _get_colors(self, skin_tone, style):
        """Get appropriate colors based on skin tone and style"""
        # Default to medium skin tone if not found
        if skin_tone not in self.color_palettes:
            skin_tone = "medium" if "dark" in skin_tone else "light"

        palette = self.color_palettes[skin_tone]

        # Default to casual if style not found
        if style not in palette:
            style = "casual"

        return {
            "main": random.choice(palette[style]),
            "accent": random.choice(
                palette["accent"] if "accent" in palette else palette[style]
            ),
        }

    def _modify_for_weather(self, items, weather):
        """Modify clothing recommendations based on weather"""
        if weather not in self.weather_modifiers:
            return items

        modifiers = self.weather_modifiers[weather]

        # Apply material modifier
        material = random.choice(modifiers["materials"])
        items["material"] = material

        # Apply style modifier
        style = random.choice(modifiers["styles"])

        # Modify top description based on weather
        items["top"] = f"{items['top']} {style} berbahan {material}"

        return items

    def _format_response(self, items, colors, parameters):
        """Format the final response using templates"""
        gender = parameters.get("gender", "neutral")
        skin_tone = parameters.get("skin_tone", "neutral")
        occasion = parameters.get("occasion", "")
        style = self._determine_style(occasion)

        # Select appropriate template
        if style in self.occasion_templates:
            template = random.choice(self.occasion_templates[style])
        else:
            template = random.choice(self.templates)

        # Format response with all parameters
        response = template.format(
            occasion=occasion,
            gender=gender,
            skin_tone=skin_tone,
            top=items["top"],
            top_color=colors["main"],
            bottom=items["bottom"],
            shoes=items["shoes"],
            accessory=items.get("accessory", "aksesoris yang sesuai"),
            material=items.get("material", ""),
        )

        return response


# Usage example
if __name__ == "__main__":
    generator = ResponseGenerator()

    # Test different combinations
    test_cases = [
        {"gender": "pria", "skin_tone": "light", "occasion": "interview kerja"},
        {"gender": "wanita", "skin_tone": "dark", "occasion": "pesta formal"},
        {"gender": "pria", "skin_tone": "very_dark", "occasion": "hangout casual"},
        {"gender": "wanita", "skin_tone": "very_light", "occasion": "meeting kantor"},
        {
            "gender": "pria",
            "skin_tone": "medium",
            "occasion": "cuaca panas",
            "weather": "hot",
        },
    ]

    print("Fashion Recommendation Examples:\n")
    for i, case in enumerate(test_cases, 1):
        response = generator.generate_response(case)
        print(f"Example {i}: {case}")
        print(f"Response: {response}\n")
