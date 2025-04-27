# src/dataset_generator.py
import pandas as pd
import random
from typing import List, Dict
import itertools
import os


class FashionDatasetGenerator:
    def __init__(self):
        self.skin_tones = {
            "light": ["cerah", "putih", "kuning langsat"],
            "dark": ["sawo matang", "gelap", "coklat"],
            "neutral": [""],
        }

        self.genders = {
            "pria": ["pria", "laki-laki", "cowok"],
            "wanita": ["wanita", "perempuan", "cewek"],
            "neutral": [""],
        }

        self.color_palettes = {
            "light": {
                "formal": [
                    "navy blue",
                    "charcoal grey",
                    "deep burgundy",
                    "forest green",
                    "royal purple",
                ],
                "casual": [
                    "pastel blue",
                    "mint green",
                    "lavender",
                    "light pink",
                    "powder blue",
                ],
                "accent": [
                    "rose gold",
                    "silver",
                    "pearl white",
                    "soft pink",
                    "light grey",
                ],
            },
            "dark": {
                "formal": [
                    "chocolate brown",
                    "olive green",
                    "deep gold",
                    "terracotta",
                    "rust orange",
                ],
                "casual": [
                    "bright yellow",
                    "coral",
                    "electric blue",
                    "emerald green",
                    "rich purple",
                ],
                "accent": ["gold", "bronze", "copper", "bright red", "royal blue"],
            },
        }

        self.seasonal_colors = {
            "spring": {
                "colors": {
                    "main": [
                        "pastel pink",
                        "mint green",
                        "light yellow",
                        "baby blue",
                        "lavender",
                        "peach",
                        "soft coral",
                        "light aqua",
                    ],
                    "accent": [
                        "white",
                        "light grey",
                        "cream",
                        "rose gold",
                        "pale gold",
                    ],
                },
                "fabrics": ["katun ringan", "linen", "chiffon", "sifon tipis"],
                "patterns": [
                    "floral kecil",
                    "polkadot",
                    "garis tipis",
                    "motif bunga sakura",
                ],
            },
            "summer": {
                "colors": {
                    "main": [
                        "bright white",
                        "sky blue",
                        "coral",
                        "turquoise",
                        "bright yellow",
                        "sea foam green",
                        "hot pink",
                        "vibrant orange",
                    ],
                    "accent": ["metallic silver", "bright gold", "pearl white", "aqua"],
                },
                "fabrics": ["katun", "linen ringan", "jersey", "rayon"],
                "patterns": ["tropical", "garis-garis", "tie-dye", "abstrak cerah"],
            },
            "autumn": {
                "colors": {
                    "main": [
                        "burgundy",
                        "forest green",
                        "rust orange",
                        "mustard yellow",
                        "deep brown",
                        "olive green",
                        "terracotta",
                        "deep purple",
                    ],
                    "accent": ["copper", "bronze", "antique gold", "deep red"],
                },
                "fabrics": ["wool", "suede", "corduroy", "flannel"],
                "patterns": [
                    "plaid",
                    "motif daun",
                    "kotak-kotak",
                    "abstrak earth tone",
                ],
            },
            "winter": {
                "colors": {
                    "main": [
                        "pure white",
                        "navy blue",
                        "black",
                        "charcoal grey",
                        "deep red",
                        "emerald green",
                        "royal blue",
                        "ice blue",
                    ],
                    "accent": ["silver", "platinum", "white gold", "deep purple"],
                },
                "fabrics": ["wool tebal", "velvet", "cashmere", "kulit"],
                "patterns": ["solid", "geometris", "metalik", "tweed"],
            },
        }

        self.seasonal_outfits = {
            "spring": {
                "pria": [
                    "kemeja lengan pendek {color} dengan celana chino dan loafers",
                    "polo shirt {color} dengan celana linen dan sneakers putih",
                    "kemeja {pattern} dengan celana katun dan sepatu canvas",
                    "kaos {color} dengan cardigan ringan dan celana bahan",
                ],
                "wanita": [
                    "dress {pattern} berbahan {fabric} dengan flat shoes",
                    "blus {color} dengan rok midi dan sandal",
                    "kemeja {color} dengan celana kulot dan sepatu slip-on",
                    "jumpsuit {color} dengan wedges",
                ],
            },
            "summer": {
                "pria": [
                    "kaos {color} dengan celana pendek dan sandal",
                    "kemeja {pattern} berbahan {fabric} dengan celana pendek dan espadrilles",
                    "tank top {color} dengan celana pantai dan sandal",
                    "polo shirt {color} dengan bermuda shorts dan boat shoes",
                ],
                "wanita": [
                    "dress maxi {pattern} dengan sandal",
                    "crop top {color} dengan rok midi dan flat sandals",
                    "blus tanpa lengan {color} dengan celana pendek",
                    "romper {pattern} dengan sandal gladiator",
                ],
            },
            "autumn": {
                "pria": [
                    "sweater {color} dengan jeans dan chelsea boots",
                    "kemeja flanel {pattern} dengan chinos dan sepatu boots",
                    "turtleneck {color} dengan blazer dan celana bahan",
                    "jaket kulit dengan kaos {color} dan jeans",
                ],
                "wanita": [
                    "sweater dress {color} dengan boots tinggi",
                    "turtleneck {color} dengan rok midi dan ankle boots",
                    "blazer {color} dengan sweater dan celana bahan",
                    "kemeja {pattern} dengan cardigan dan jeans",
                ],
            },
            "winter": {
                "pria": [
                    "mantel panjang {color} dengan sweater dan celana wool",
                    "jaket tebal {color} dengan turtleneck dan celana bahan",
                    "coat {color} dengan syal dan sarung tangan senada",
                    "jaket bomber dengan sweater {color} dan celana tebal",
                ],
                "wanita": [
                    "long coat {color} dengan dress rajut dan boots",
                    "sweater turtleneck {color} dengan rok panjang dan boots",
                    "jaket tebal {color} dengan celana wool dan boots tinggi",
                    "mantel {color} dengan syal {pattern} dan sarung tangan",
                ],
            },
        }

        self.seasonal_queries = [
            "Apa yang cocok dipakai di {season} untuk {gender}?",
            "Rekomendasi outfit {season} untuk {gender}?",
            "Fashion {season} yang bagus untuk {gender}?",
            "Style yang cocok untuk {season}?",
            "Pakaian yang nyaman untuk {season}?",
            "Outfit {season} yang trendy?",
            "Apa yang sebaiknya dipakai saat {season}?",
            "Rekomendasi warna untuk {season}?",
            "Kombinasi warna yang bagus untuk {season}?",
            "Pattern yang cocok untuk {season}?",
        ]

        self.templates = {
            "query_templates": [
                "Apa yang cocok untuk {occasion} untuk {gender} berkulit {skin_tone}?",
                "Rekomendasi pakaian {occasion} untuk {gender} dengan kulit {skin_tone}?",
                "Pakaian untuk {occasion}?",
                "Outfit untuk {occasion}?",
                "Apa yang sebaiknya dipakai untuk {occasion}?",
                "Baju untuk {occasion}?",
                "Bagaimana cara berpakaian untuk {gender} berkulit {skin_tone} ke {occasion}?",
                "Outfit yang bagus untuk {gender} dengan kulit {skin_tone} ke {occasion}?",
                "Saya {gender} berkulit {skin_tone} mau pergi ke {occasion}, sebaiknya pakai apa ya?",
                "{gender} berkulit {skin_tone} mau ke {occasion}, enaknya pakai baju apa?",
            ],
            "occasions": {
                # Formal Categories - Light Skin
                "formal_pria_light": {
                    "events": [
                        "interview kerja",
                        "rapat formal",
                        "seminar bisnis",
                        "presentasi perusahaan",
                        "acara kantoran",
                    ],
                    "responses": [
                        "kenakan setelan jas navy blue dengan kemeja putih dan sepatu pantofel hitam",
                        "kombinasikan blazer gelap dengan kemeja light blue dan celana bahan",
                    ],
                    "label": 0,
                    "gender": "pria",
                    "skin_tone": "light",
                },
                "formal_wanita_light": {
                    "events": [
                        "interview kerja wanita",
                        "rapat formal wanita",
                        "seminar wanita",
                    ],
                    "responses": [
                        "kenakan blazer dengan rok pensil dan sepatu heels",
                        "padukan blus formal dengan celana bahan dan flat shoes formal",
                    ],
                    "label": 1,
                    "gender": "wanita",
                    "skin_tone": "light",
                },
                # Formal Categories - Dark Skin
                "formal_pria_dark": {
                    "events": [
                        "presentasi formal",
                        "seminar bisnis",
                    ],
                    "responses": [
                        "gunakan setelan jas abu-abu dengan dasi merah dan sepatu pantofel hitam",
                        "kenakan blazer hitam dengan kemeja putih dan celana bahan gelap",
                    ],
                    "label": 2,
                    "gender": "pria",
                    "skin_tone": "dark",
                },
                "formal_wanita_dark": {
                    "events": [
                        "acara formal wanita",
                        "rapat formal wanita",
                    ],
                    "responses": [
                        "gunakan setelan blazer pastel dengan rok midi dan sepatu hak tinggi",
                        "kenakan dress formal dengan warna gelap dan aksesoris minimalis",
                    ],
                    "label": 3,
                    "gender": "wanita",
                    "skin_tone": "dark",
                },
                # Casual Categories - Light Skin
                "kasual_pria_light": {
                    "events": [
                        "jalan-jalan santai",
                        "hangout",
                    ],
                    "responses": [
                        "kenakan kaos dengan jeans dan sneakers casual",
                        "padukan kemeja casual dengan chino pants dan sepatu sneakers",
                    ],
                    "label": 4,
                    "gender": "pria",
                    "skin_tone": "light",
                },
                "kasual_wanita_light": {
                    "events": [
                        "jalan-jalan santai wanita",
                        "nongkrong casual",
                    ],
                    "responses": [
                        "kenakan dress casual dengan flat shoes nyaman",
                        "padukan kaos dengan rok A-line dan sneakers",
                    ],
                    "label": 5,
                    "gender": "wanita",
                    "skin_tone": "light",
                },
                # Casual Categories - Dark Skin
                "kasual_pria_dark": {
                    "events": [
                        "jalan santai pria",
                        "nongkrong di kafe",
                    ],
                    "responses": [
                        "gunakan t-shirt hitam dengan jeans biru dan sneakers putih",
                        "padukan polo shirt dengan celana pendek khaki dan sandal santai",
                    ],
                    "label": 6,
                    "gender": "pria",
                    "skin_tone": "dark",
                },
                "kasual_wanita_dark": {
                    "events": [
                        "jalan-jalan wanita",
                        "nongkrong malam wanita",
                    ],
                    "responses": [
                        "kombinasikan blouse casual dengan celana jeans dan sepatu flat",
                        "gunakan dress maxi dengan warna cerah dan sandal nyaman",
                    ],
                    "label": 7,
                    "gender": "wanita",
                    "skin_tone": "dark",
                },
                # General Event Categories
                "wedding": {
                    "events": [
                        "pernikahan",
                        "resepsi nikah",
                    ],
                    "responses": [
                        "kenakan gaun panjang dengan heels dan clutch bag",
                        "padukan kebaya modern dengan rok panjang dan selop",
                    ],
                    "label": 8,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                "party": {
                    "events": [
                        "pesta ulang tahun",
                        "party malam",
                    ],
                    "responses": [
                        "kenakan dress party dengan aksesoris berkilau",
                        "padukan kemeja fancy dengan celana formal",
                    ],
                    "label": 9,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                "business_meeting": {
                    "events": [
                        "rapat bisnis",
                        "konferensi bisnis",
                    ],
                    "responses": [
                        "gunakan setelan jas abu-abu dengan kemeja putih",
                        "kombinasikan blazer navy dengan celana bahan hitam",
                    ],
                    "label": 10,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                # Weather Categories
                "hot_weather": {
                    "events": [
                        "cuaca panas",
                        "musim kemarau",
                    ],
                    "responses": [
                        "kenakan pakaian berbahan katun yang menyerap keringat",
                        "gunakan kaos lengan pendek dengan celana pendek",
                    ],
                    "label": 11,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                "cold_weather": {
                    "events": [
                        "cuaca dingin",
                        "musim dingin",
                    ],
                    "responses": [
                        "kenakan sweater tebal dengan celana panjang",
                        "gunakan pakaian berlapis dengan mantel hangat",
                    ],
                    "label": 12,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                "rainy_weather": {
                    "events": [
                        "cuaca hujan",
                        "gerimis",
                    ],
                    "responses": [
                        "kenakan jas hujan dengan sepatu anti air",
                        "gunakan jaket waterproof dengan celana panjang",
                    ],
                    "label": 13,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                "windy_weather": {
                    "events": [
                        "cuaca berangin",
                        "angin kencang",
                    ],
                    "responses": [
                        "kenakan jaket windbreaker dengan celana panjang",
                        "gunakan pakaian berlapis dengan jaket tahan angin",
                    ],
                    "label": 14,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                # Season Categories
                "summer": {
                    "events": [
                        "musim panas",
                        "liburan musim panas",
                    ],
                    "responses": [
                        "kenakan kaos ringan dengan celana pendek dan sandal",
                        "gunakan pakaian berwarna cerah dengan bahan breathable",
                    ],
                    "label": 15,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                "winter": {
                    "events": [
                        "musim dingin",
                        "liburan musim dingin",
                    ],
                    "responses": [
                        "kenakan jaket tebal dengan celana wool",
                        "gunakan mantel dengan syal dan sepatu boots",
                    ],
                    "label": 16,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                "spring": {
                    "events": [
                        "musim semi",
                        "awal musim semi",
                    ],
                    "responses": [
                        "kenakan dress floral dengan cardigan ringan",
                        "gunakan blus dengan rok midi dan flat shoes",
                    ],
                    "label": 17,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                "autumn": {
                    "events": [
                        "musim gugur",
                        "suasana gugur",
                    ],
                    "responses": [
                        "kenakan sweater rajut dengan celana panjang",
                        "padukan jaket kulit dengan jeans dan boots",
                    ],
                    "label": 18,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
                # Other Categories
                "other": {
                    "events": [
                        "acara lainnya",
                        "kegiatan umum",
                    ],
                    "responses": [
                        "gunakan pakaian yang nyaman dan sesuai situasi",
                        "pilih pakaian casual atau formal tergantung kebutuhan",
                    ],
                    "label": 19,
                    "gender": "neutral",
                    "skin_tone": "neutral",
                },
            },
        }

    def generate_variation(
        self, template: str, occasion: str, gender: str, skin_tone: str
    ) -> str:
        """Generate variations of queries with different wordings"""
        gender_term = random.choice(self.genders[gender]) if gender != "neutral" else ""
        skin_tone_term = (
            random.choice(self.skin_tones[skin_tone]) if skin_tone != "neutral" else ""
        )
        if gender == "neutral" and skin_tone == "neutral":
            return f"Apa yang cocok untuk {occasion}?"

        return template.format(
            occasion=occasion, gender=gender_term, skin_tone=skin_tone_term
        )

    def generate_color_recommendation(self, skin_tone: str, occasion_type: str) -> str:
        if skin_tone in ["light", "dark"]:
            colors = self.color_palettes[skin_tone]
            if "formal" in occasion_type.lower():
                recommended_colors = colors["formal"]
                accent_colors = colors["accent"]
            else:
                recommended_colors = colors["casual"]
                accent_colors = colors["accent"]

            main_color = random.choice(recommended_colors)
            accent_color = random.choice(accent_colors)

            return f" - pilih warna {main_color} sebagai warna utama dan {accent_color} sebagai aksen"
        return ""

    def generate_skin_tone_gender_dataset(self, samples_per_combination: int = 50):
        dataset = []

        # Define skin tones with more granularity
        additional_skin_tones = {
            "very_light": ["sangat cerah", "putih pucat", "kulit putih"],
            "medium": ["sawo matang muda", "kuning kecoklatan", "tan"],
            "very_dark": ["coklat tua", "hitam manis", "kulit gelap"],
        }

        # Extended color recommendations for different skin tones
        extended_color_recommendations = {
            "very_light": {
                "best": ["navy blue", "burgundy", "emerald green", "royal purple"],
                "avoid": ["neon yellow", "light beige", "pale pastels"],
            },
            "light": {
                "best": ["deep blue", "forest green", "plum", "berry tones"],
                "avoid": ["orange-yellow", "bright orange", "beige"],
            },
            "medium": {
                "best": ["coral", "teal", "warm purple", "olive green"],
                "avoid": ["brown close to skin tone", "muted pastel"],
            },
            "dark": {
                "best": ["bright yellow", "fuchsia", "cobalt blue", "bright orange"],
                "avoid": ["chocolate brown", "dark navy", "muted earth tones"],
            },
            "very_dark": {
                "best": ["bright white", "electric blue", "hot pink", "lime green"],
                "avoid": ["dark brown", "deep navy", "black"],
            },
        }

        # Query templates specifically for color advice
        color_query_templates = [
            "Warna apa yang cocok untuk {gender} dengan kulit {skin_tone}?",
            "Warna yang bagus untuk {gender} berkulit {skin_tone}?",
            "Saya {gender} dengan warna kulit {skin_tone}, warna apa yang flattering?",
            "Rekomendasi warna pakaian untuk {gender} dengan tone kulit {skin_tone}?",
            "Kombinasi warna untuk {gender} dengan kulit {skin_tone}?",
            "{gender} berkulit {skin_tone} sebaiknya mengenakan warna apa?",
        ]

        # Generate specific queries for standard skin tones
        for skin_tone in ["light", "dark"]:
            for gender in ["pria", "wanita"]:
                for _ in range(samples_per_combination):
                    # Create color-specific queries
                    template = random.choice(color_query_templates)
                    skin_tone_term = random.choice(self.skin_tones[skin_tone])
                    gender_term = random.choice(self.genders[gender])

                    query = template.format(
                        gender=gender_term, skin_tone=skin_tone_term
                    )

                    # Create detailed color recommendations
                    best_colors = extended_color_recommendations[skin_tone]["best"]
                    avoid_colors = extended_color_recommendations[skin_tone]["avoid"]

                    response = f"Untuk {gender_term} dengan kulit {skin_tone_term}, "
                    response += f"warna yang sangat cocok adalah {', '.join(random.sample(best_colors, 2))}. "
                    response += f"Sebaiknya hindari {', '.join(random.sample(avoid_colors, 2))} "
                    response += f"karena kurang flattering untuk tone kulit Anda."

                    # Map to appropriate label
                    label_map = {
                        ("pria", "light"): 0,
                        ("wanita", "light"): 1,
                        ("pria", "dark"): 2,
                        ("wanita", "dark"): 3,
                    }

                    label = label_map.get((gender, skin_tone), 19)

                    dataset.append(
                        {
                            "query": query,
                            "response": response,
                            "label": label,
                            "gender": gender,
                            "skin_tone": skin_tone,
                        }
                    )

        # Add additional skin tone variations
        for skin_tone, tone_terms in additional_skin_tones.items():
            for gender in ["pria", "wanita"]:
                for _ in range(
                    samples_per_combination // 2
                ):  # Half as many samples for extended tones
                    template = random.choice(color_query_templates)
                    skin_tone_term = random.choice(tone_terms)
                    gender_term = random.choice(self.genders[gender])

                    query = template.format(
                        gender=gender_term, skin_tone=skin_tone_term
                    )

                    best_colors = extended_color_recommendations[skin_tone]["best"]
                    avoid_colors = extended_color_recommendations[skin_tone]["avoid"]

                    response = f"Untuk {gender_term} dengan kulit {skin_tone_term}, "
                    response += f"warna yang sangat cocok adalah {', '.join(random.sample(best_colors, 2))}. "
                    response += f"Sebaiknya hindari {', '.join(random.sample(avoid_colors, 2))} "
                    response += f"karena kurang flattering untuk tone kulit Anda."

                    # Map to closest standard category
                    if skin_tone == "very_light":
                        label = 0 if gender == "pria" else 1  # Map to light
                    else:  # medium, very_dark
                        label = 2 if gender == "pria" else 3  # Map to dark

                    dataset.append(
                        {
                            "query": query,
                            "response": response,
                            "label": label,
                            "gender": gender,
                            "skin_tone": skin_tone,
                        }
                    )

        return pd.DataFrame(dataset)

    def generate_dataset(self, samples_per_category: int = 200) -> pd.DataFrame:
        dataset = []

        for occasion_type, details in self.templates["occasions"].items():
            # Determine number of samples based on category type
            if details["gender"] == "neutral" and details["skin_tone"] == "neutral":
                current_samples = (
                    samples_per_category * 2
                )  # Double the samples for neutral categories
            else:
                current_samples = samples_per_category

            for _ in range(current_samples):
                event = random.choice(details["events"])

                # For neutral categories (weather, general events)
                if details["gender"] == "neutral" and details["skin_tone"] == "neutral":
                    # Generate multiple variations for neutral categories
                    templates = [
                        f"Apa yang cocok untuk {event}?",
                        f"Rekomendasi pakaian untuk {event}?",
                        f"Bagaimana cara berpakaian untuk {event}?",
                        f"Outfit yang bagus untuk {event}?",
                        f"Mau ke {event}, sebaiknya pakai apa ya?",
                    ]
                    query = random.choice(templates)
                else:
                    template = random.choice(self.templates["query_templates"])
                    query = self.generate_variation(
                        template, event, details["gender"], details["skin_tone"]
                    )

                response = random.choice(details["responses"])
                if details["skin_tone"] in ["light", "dark"]:
                    color_rec = self.generate_color_recommendation(
                        details["skin_tone"], occasion_type
                    )
                    response = response + color_rec

                dataset.append(
                    {
                        "query": query,
                        "response": response,
                        "label": details["label"],
                        "gender": details["gender"],
                        "skin_tone": details["skin_tone"],
                    }
                )

                # Add variations with higher probability for neutral categories
                variation_prob = 0.6 if details["gender"] == "neutral" else 0.3
                if random.random() < variation_prob:
                    if details["gender"] == "neutral":
                        variant_template = random.choice(templates)
                    else:
                        variant_template = random.choice(
                            self.templates["query_templates"]
                        )
                        variant_template = self.generate_variation(
                            variant_template,
                            event,
                            details["gender"],
                            details["skin_tone"],
                        )

                    dataset.append(
                        {
                            "query": variant_template,
                            "response": response,
                            "label": details["label"],
                            "gender": details["gender"],
                            "skin_tone": details["skin_tone"],
                        }
                    )

        return pd.DataFrame(dataset)


def combine_with_original_dataset():
    # Load original dataset
    original_df = pd.read_csv("train/dataset.csv")
    print(f"Original dataset size: {len(original_df)}")

    # Add gender and skin_tone columns to original dataset if they don't exist
    if "gender" not in original_df.columns:
        original_df["gender"] = "neutral"
    if "skin_tone" not in original_df.columns:
        original_df["skin_tone"] = "neutral"

    generator = FashionDatasetGenerator()
    generated_df = generator.generate_dataset(samples_per_category=150)
    print(f"General dataset size: {len(generated_df)}")

    # Generate specific skin tone and gender data
    skin_tone_df = generator.generate_skin_tone_gender_dataset(
        samples_per_combination=100
    )
    print(f"Skin tone specific dataset size: {len(skin_tone_df)}")

    # Combine datasets
    combined_df = pd.concat(
        [original_df, generated_df, skin_tone_df], ignore_index=True
    )

    # Remove duplicates
    combined_df = combined_df.drop_duplicates(subset=["query"])
    print(f"Combined dataset size after removing duplicates: {len(combined_df)}")

    # Save combined dataset
    os.makedirs("data/processed", exist_ok=True)
    combined_df.to_csv("data/processed/combined_dataset.csv", index=False)
    print("Combined dataset saved to data/processed/combined_dataset.csv")

    # Print distribution
    print("\nLabel distribution in combined dataset:")
    label_counts = combined_df["label"].value_counts().sort_index()
    for label, count in label_counts.items():
        print(f"Label {label}: {count} examples")

    print("\nGender distribution:")
    gender_counts = combined_df["gender"].value_counts()
    for gender, count in gender_counts.items():
        print(f"{gender}: {count} examples")

    print("\nSkin tone distribution:")
    skin_tone_counts = combined_df["skin_tone"].value_counts()
    for tone, count in skin_tone_counts.items():
        print(f"{tone}: {count} examples")


if __name__ == "__main__":
    combine_with_original_dataset()
