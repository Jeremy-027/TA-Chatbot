# src/fashion_mapping.py
import random

fashion_mapping = {
    "occasion_mappings": {
        # FORMAL OCCASIONS
        "formal": {
            # FOR LIGHT SKIN TONES
            "light": {
                "pria": {
                    "tops": [
                        "jas navy blue",
                        "blazer charcoal gray",
                        "kemeja putih crisp",
                        "kemeja light blue",
                    ],
                    "bottoms": [
                        "celana bahan hitam",
                        "celana formal navy",
                        "celana wool abu-abu",
                    ],
                    "shoes": [
                        "sepatu oxford hitam",
                        "sepatu pantofel coklat tua",
                        "loafers hitam",
                    ],
                    "accessories": [
                        "dasi sutra navy",
                        "dasi burgundy",
                        "jam tangan silver",
                        "ikat pinggang hitam formal",
                    ],
                    "colors_best": [
                        "navy blue",
                        "burgundy",
                        "forest green",
                        "charcoal grey",
                        "deep purple",
                    ],
                    "colors_avoid": ["orange-yellow", "neon colors", "light beige"],
                    "tips": "Warna gelap seperti navy blue dan charcoal akan memberikan kontras yang bagus dengan tone kulit cerah Anda.",
                },
                "wanita": {
                    "tops": [
                        "blazer navy fitted",
                        "blus sutra putih",
                        "kemeja wanita light blue",
                        "blus formal pastel",
                    ],
                    "bottoms": [
                        "rok pensil hitam",
                        "celana bahan straight-cut",
                        "rok midi navy",
                    ],
                    "shoes": [
                        "pumps hitam",
                        "heels medium nude",
                        "flat shoes hitam formal",
                    ],
                    "accessories": [
                        "pearl necklace",
                        "earrings silver simple",
                        "tas formal structured",
                        "scarf sutra",
                    ],
                    "colors_best": [
                        "navy blue",
                        "burgundy",
                        "emerald green",
                        "soft pink",
                        "lavender",
                    ],
                    "colors_avoid": [
                        "neon yellow",
                        "bright orange",
                        "beige terlalu terang",
                    ],
                    "tips": "Padukan warna-warna jewel tone dengan aksesori silver atau rose gold untuk tampilan formal yang elegan.",
                },
            },
            # FOR DARK SKIN TONES
            "dark": {
                "pria": {
                    "tops": [
                        "jas abu-abu",
                        "blazer coklat tua",
                        "kemeja putih",
                        "kemeja biru muda",
                    ],
                    "bottoms": [
                        "celana bahan hitam",
                        "celana formal coklat tua",
                        "celana wool abu-abu",
                    ],
                    "shoes": [
                        "sepatu oxford coklat",
                        "sepatu pantofel hitam",
                        "loafers dark burgundy",
                    ],
                    "accessories": [
                        "dasi maroon",
                        "dasi olive green",
                        "jam tangan gold",
                        "ikat pinggang formal coklat",
                    ],
                    "colors_best": [
                        "rich brown",
                        "olive green",
                        "deep gold",
                        "terracotta",
                        "rust orange",
                    ],
                    "colors_avoid": [
                        "dark brown persis tone kulit",
                        "navy terlalu gelap",
                        "abu-abu muda",
                    ],
                    "tips": "Warna-warna earth tone seperti olive green dan terracotta akan sangat menonjolkan tone kulit Anda.",
                },
                "wanita": {
                    "tops": [
                        "blazer cream",
                        "blus formal berwarna terang",
                        "kemeja wanita putih",
                        "blazer terracotta",
                    ],
                    "bottoms": [
                        "rok pensil hitam",
                        "celana bahan camel",
                        "rok midi dark olive",
                    ],
                    "shoes": ["pumps nude", "heels coklat", "flat shoes hitam"],
                    "accessories": [
                        "gold statement earrings",
                        "kalung gold",
                        "tas formal structured",
                        "scarf patterned",
                    ],
                    "colors_best": [
                        "turquoise",
                        "bright yellow",
                        "coral",
                        "emerald green",
                        "royal purple",
                    ],
                    "colors_avoid": [
                        "dark brown persis tone kulit",
                        "olive pucat",
                        "khaki",
                    ],
                    "tips": "Warna-warna cerah dan vibrant akan sangat menonjolkan keindahan tone kulit Anda.",
                },
            },
        },
        # CASUAL OCCASIONS
        "casual": {
            # FOR LIGHT SKIN TONES
            "light": {
                "pria": {
                    "tops": [
                        "polo shirt navy",
                        "t-shirt putih",
                        "kemeja casual chambray",
                        "sweater rajut burgundy",
                    ],
                    "bottoms": [
                        "jeans indigo",
                        "chinos khaki",
                        "celana pendek navy",
                        "celana linen",
                    ],
                    "shoes": [
                        "sneakers putih",
                        "boat shoes",
                        "desert boots",
                        "loafers casual",
                    ],
                    "accessories": [
                        "jam tangan casual",
                        "topi baseball",
                        "kacamata hitam",
                        "gelang kulit",
                    ],
                    "colors_best": [
                        "pastel blue",
                        "salmon pink",
                        "mint green",
                        "lavender",
                        "soft yellow",
                    ],
                    "colors_avoid": [
                        "kuning terlalu terang",
                        "off-white",
                        "cream pucat",
                    ],
                    "tips": "Warna-warna pastel dan medium akan memberikan kontras lembut dengan tone kulit cerah Anda.",
                },
                "wanita": {
                    "tops": [
                        "blus pastel",
                        "t-shirt fitted",
                        "kemeja denim",
                        "sweater rajut pink",
                    ],
                    "bottoms": [
                        "jeans high-waist",
                        "rok A-line",
                        "culottes",
                        "shorts denim",
                    ],
                    "shoes": [
                        "sneakers putih",
                        "sandal flat",
                        "ankle boots",
                        "espadrilles",
                    ],
                    "accessories": [
                        "tas selempang",
                        "kalung simple",
                        "scrunchies",
                        "bandana",
                    ],
                    "colors_best": [
                        "blush pink",
                        "baby blue",
                        "mint green",
                        "lavender",
                        "peach",
                    ],
                    "colors_avoid": ["beige pucat", "kuning neon", "putih polos"],
                    "tips": "Warna-warna soft pastel dan bright akan memberikan look yang segar pada tone kulit cerah Anda.",
                },
            },
            # FOR DARK SKIN TONES
            "dark": {
                "pria": {
                    "tops": [
                        "t-shirt bright colors",
                        "polo shirt vibrant",
                        "kemeja motif",
                        "hoodie colorful",
                    ],
                    "bottoms": [
                        "jeans hitam",
                        "chinos berwarna",
                        "cargo pants",
                        "track pants",
                    ],
                    "shoes": [
                        "sneakers colorful",
                        "high-tops",
                        "sandal",
                        "boots casual",
                    ],
                    "accessories": [
                        "topi snapback",
                        "kacamata colorful",
                        "bandana",
                        "gelang paracord",
                    ],
                    "colors_best": [
                        "bright yellow",
                        "royal blue",
                        "red",
                        "teal",
                        "bright green",
                    ],
                    "colors_avoid": ["coklat tua", "khaki gelap", "olive gelap"],
                    "tips": "Warna-warna cerah dan vibrant akan memberikan kontras yang menarik dengan tone kulit Anda.",
                },
                "wanita": {
                    "tops": [
                        "crop top colorful",
                        "blus warna cerah",
                        "t-shirt graphic",
                        "kemeja off-shoulder",
                    ],
                    "bottoms": [
                        "jeans colorful",
                        "rok warna cerah",
                        "leggings patterned",
                        "shorts high-waist",
                    ],
                    "shoes": [
                        "sneakers colorful",
                        "sandal gladiator",
                        "flatform shoes",
                        "boots colorful",
                    ],
                    "accessories": [
                        "statement earrings",
                        "bandana colorful",
                        "tas mini colorful",
                        "kacamata oversized",
                    ],
                    "colors_best": [
                        "bright orange",
                        "hot pink",
                        "lime green",
                        "cobalt blue",
                        "bright yellow",
                    ],
                    "colors_avoid": [
                        "brown mirip warna kulit",
                        "beige gelap",
                        "olive abu-abu",
                    ],
                    "tips": "Warna-warna cerah dan jewel tones akan membuat penampilan Anda lebih pop dan menonjolkan tone kulit indah Anda.",
                },
            },
        },
    },
    # WEATHER RECOMMENDATIONS
    "weather_mappings": {
        "hot_weather": {
            "materials": ["katun", "linen", "chambray", "seersucker", "rayon"],
            "styles": [
                "loose fit",
                "sleeveless",
                "short sleeve",
                "cropped",
                "breathable",
            ],
            "tips": "Pilih bahan ringan dan breathable seperti katun dan linen. Hindari lapisan berlebih dan warna hitam yang menyerap panas.",
        },
        "cold_weather": {
            "materials": ["wool", "cashmere", "fleece", "corduroy", "leather"],
            "styles": ["layered", "turtleneck", "long sleeve", "insulated", "lined"],
            "tips": "Lapisan pakaian (layering) adalah kunci untuk tetap hangat. Mulailah dengan bahan yang menyerap kelembaban dekat kulit.",
        },
        "rainy_weather": {
            "materials": [
                "polyester",
                "nylon",
                "gore-tex",
                "waterproof cotton",
                "polyurethane coated",
            ],
            "styles": [
                "hooded",
                "water-resistant",
                "quick-dry",
                "covered",
                "sealed seams",
            ],
            "tips": "Hindari bahan yang menyerap air seperti denim dan katun biasa. Pilih pakaian waterproof atau water-resistant.",
        },
    },
    # SEASONAL RECOMMENDATIONS
    "seasonal_mappings": {
        "spring": {
            "colors": ["pastel pink", "light blue", "mint green", "lavender", "yellow"],
            "patterns": ["floral", "small prints", "gingham", "light stripes"],
            "materials": ["light cotton", "linen blend", "light denim", "chiffon"],
            "tips": "Musim semi ideal untuk warna-warna pastel dan pola floral. Siapkan juga light jacket untuk perubahan cuaca.",
        },
        "summer": {
            "colors": ["white", "bright blue", "coral", "yellow", "turquoise"],
            "patterns": ["tropical", "tie-dye", "bold stripes", "colorblocking"],
            "materials": ["lightweight cotton", "linen", "jersey", "mesh"],
            "tips": "Utamakan kenyamanan dengan bahan ringan dan breathable. UV protection juga penting untuk aktivitas outdoor.",
        },
        "autumn": {
            "colors": [
                "burgundy",
                "mustard yellow",
                "forest green",
                "rust orange",
                "brown",
            ],
            "patterns": ["plaid", "houndstooth", "herringbone", "leaf patterns"],
            "materials": ["light wool", "corduroy", "suede", "flannel"],
            "tips": "Earth tones dan bahan yang lebih tebal mulai relevan. Layering sangat berguna untuk perubahan suhu.",
        },
        "winter": {
            "colors": ["deep red", "emerald green", "navy", "charcoal", "black"],
            "patterns": ["fair isle", "tartan", "geometric", "solid colors"],
            "materials": ["heavy wool", "cashmere", "fleece", "down", "velvet"],
            "tips": "Prioritaskan kehangatan dengan material insulating. Teknik layering sangat penting di musim dingin.",
        },
    },
}


class FashionMapping:
    def __init__(self):
        self.fashion_mapping = fashion_mapping

    def get_recommendation(self, parameters):
        """Get clothing recommendations based on parameters"""
        gender = parameters.get("gender", "pria")
        skin_tone = parameters.get("skin_tone", "light")
        occasion = parameters.get("occasion", "casual")
        weather = parameters.get("weather", None)
        season = parameters.get("season", None)

        recommendation = {}

        # Get basic occasion recommendation
        if occasion in self.fashion_mapping["occasion_mappings"]:
            if skin_tone in self.fashion_mapping["occasion_mappings"][occasion]:
                if (
                    gender
                    in self.fashion_mapping["occasion_mappings"][occasion][skin_tone]
                ):
                    recommendation = self.fashion_mapping["occasion_mappings"][
                        occasion
                    ][skin_tone][gender].copy()
                else:
                    recommendation = self.fashion_mapping["occasion_mappings"][
                        occasion
                    ][skin_tone]["pria"].copy()
            else:
                if (
                    "light" in self.fashion_mapping["occasion_mappings"][occasion]
                    and gender
                    in self.fashion_mapping["occasion_mappings"][occasion]["light"]
                ):
                    recommendation = self.fashion_mapping["occasion_mappings"][
                        occasion
                    ]["light"][gender].copy()
                else:
                    recommendation = self.fashion_mapping["occasion_mappings"][
                        "casual"
                    ]["light"]["pria"].copy()
        else:
            recommendation = self.fashion_mapping["occasion_mappings"]["casual"][
                "light"
            ]["pria"].copy()

        # Add weather-specific recommendations if applicable
        if weather and weather in self.fashion_mapping["weather_mappings"]:
            recommendation["weather_tips"] = self.fashion_mapping["weather_mappings"][
                weather
            ]["tips"]
            recommendation["materials"] = self.fashion_mapping["weather_mappings"][
                weather
            ]["materials"]
            recommendation["styles"] = self.fashion_mapping["weather_mappings"][
                weather
            ]["styles"]

        # Add seasonal recommendations if applicable
        if season and season in self.fashion_mapping["seasonal_mappings"]:
            recommendation["seasonal_colors"] = self.fashion_mapping[
                "seasonal_mappings"
            ][season]["colors"]
            recommendation["seasonal_patterns"] = self.fashion_mapping[
                "seasonal_mappings"
            ][season]["patterns"]
            recommendation["seasonal_tips"] = self.fashion_mapping["seasonal_mappings"][
                season
            ]["tips"]

        return recommendation

    def format_recommendation(self, recommendation, parameters):
        """Format recommendation into a natural language response"""
        gender = parameters.get("gender", "pria")
        skin_tone = parameters.get("skin_tone", "light")
        occasion = parameters.get("occasion", "casual")
        weather = parameters.get("weather", None)
        season = parameters.get("season", None)

        # Start building response
        response = (
            f"Untuk {gender} dengan kulit {skin_tone} yang akan menghadiri {occasion}, "
        )

        # Add main outfit recommendation
        tops = recommendation.get("tops", [])
        bottoms = recommendation.get("bottoms", [])
        shoes = recommendation.get("shoes", [])

        if tops and bottoms and shoes:
            response += f"saya merekomendasikan {random.choice(tops)} dipadukan dengan {random.choice(bottoms)} "
            response += f"dan {random.choice(shoes)}. "

        # Add color recommendation
        best_colors = recommendation.get("colors_best", [])
        avoid_colors = recommendation.get("colors_avoid", [])

        if best_colors:
            response += f"Warna yang sangat cocok untuk Anda adalah {', '.join(best_colors[:2])}. "

        if avoid_colors:
            response += f"Sebaiknya hindari {', '.join(avoid_colors[:2])}. "

        # Add accessories
        accessories = recommendation.get("accessories", [])
        if accessories:
            response += f"Lengkapi dengan {random.choice(accessories)}. "

        # Add tips
        tips = recommendation.get("tips", "")
        if tips:
            response += f"{tips} "

        # Add weather-specific advice
        if weather and "weather_tips" in recommendation:
            response += f"Karena cuaca {weather}, {recommendation['weather_tips']} "

        # Add seasonal advice
        if season and "seasonal_tips" in recommendation:
            response += f"Untuk musim {season}, {recommendation['seasonal_tips']}"

        return response
