import pandas as pd
import random
from typing import List, Dict
import itertools
import os


class FashionDatasetGenerator:
    def __init__(self):
        self.templates = {
            "query_templates": [
                "Apa yang cocok untuk {occasion}?",
                "Rekomendasi pakaian untuk {occasion}?",
                "Bagaimana cara berpakaian untuk {occasion}?",
                "Outfit yang bagus untuk {occasion}?",
                "Saya mau pergi ke {occasion}, sebaiknya pakai apa ya?",
                "Mau ke {occasion}, enaknya pakai baju apa?",
                "Pakaian apa yang cocok untuk {occasion}?",
                "Style yang bagus untuk {occasion} apa ya?",
                "Baju yang tepat untuk {occasion}?",
                "Fashion yang cocok untuk {occasion}?",
            ],
            "occasions": {
                "formal_pria": {  # Label 0
                    "events": [
                        "interview kerja",
                        "rapat formal",
                        "seminar bisnis",
                        "presentasi perusahaan",
                        "acara kantoran",
                        "meeting formal",
                        "konferensi bisnis",
                        "sidang",
                    ],
                    "responses": [
                        "kenakan setelan jas navy blue dengan kemeja putih dan sepatu pantofel hitam",
                        "kombinasikan blazer gelap dengan kemeja light blue dan celana bahan",
                        "padukan kemeja lengan panjang putih dengan celana bahan hitam dan sepatu formal",
                        "gunakan setelan jas dengan dasi dan sepatu pantofel mengkilap",
                    ],
                    "label": 0,
                },
                "formal_wanita": {  # Label 1
                    "events": [
                        "interview kerja wanita",
                        "rapat formal wanita",
                        "seminar wanita",
                        "presentasi bisnis wanita",
                        "acara formal wanita",
                    ],
                    "responses": [
                        "kenakan blazer dengan rok pensil dan sepatu heels",
                        "padukan blus formal dengan celana bahan dan flat shoes formal",
                        "kombinasikan dress formal dengan blazer dan sepatu heels medium",
                        "gunakan setelan blazer dengan rok midi dan sepatu formal",
                    ],
                    "label": 1,
                },
                "kasual_pria": {  # Label 2
                    "events": [
                        "jalan-jalan santai",
                        "hangout",
                        "nongkrong",
                        "main ke mall",
                        "weekend casual",
                        "jalan santai",
                        "kuliah",
                    ],
                    "responses": [
                        "kenakan kaos dengan jeans dan sneakers casual",
                        "padukan kemeja casual dengan chino pants dan sepatu sneakers",
                        "kombinasikan polo shirt dengan celana pendek dan sandal",
                        "gunakan t-shirt dengan celana cargo dan sepatu casual",
                    ],
                    "label": 2,
                },
                "kasual_wanita": {  # Label 3
                    "events": [
                        "jalan-jalan santai wanita",
                        "hangout wanita",
                        "nongkrong casual",
                        "mall wanita",
                        "weekend casual wanita",
                    ],
                    "responses": [
                        "kenakan dress casual dengan flat shoes nyaman",
                        "padukan kaos dengan rok A-line dan sneakers",
                        "kombinasikan blus casual dengan celana jeans dan sandal",
                        "gunakan t-shirt dengan cullotes dan sepatu flat",
                    ],
                    "label": 3,
                },
                "wedding": {  # Label 4
                    "events": [
                        "pernikahan",
                        "resepsi nikah",
                        "acara nikahan",
                        "pesta pernikahan",
                        "wedding party",
                        "nikahan teman",
                        "acara pemberkatan",
                    ],
                    "responses": [
                        "kenakan gaun panjang dengan heels dan clutch bag",
                        "padukan kebaya modern dengan rok panjang dan selop",
                        "gunakan dress formal dengan warna pastel dan sepatu hak tinggi",
                        "kombinasikan setelan jas formal dengan dasi dan sepatu pantofel mengkilap",
                    ],
                    "label": 4,
                },
                "party": {  # Label 5
                    "events": [
                        "pesta ulang tahun",
                        "party malam",
                        "pesta musik",
                        "acara gathering",
                        "year end party",
                        "pesta dansa",
                    ],
                    "responses": [
                        "kenakan dress party dengan aksesoris berkilau",
                        "padukan kemeja fancy dengan celana formal",
                        "kombinasikan blus berkilau dengan rok atau celana hitam",
                        "gunakan outfit yang eye-catching dan nyaman untuk berpesta",
                    ],
                    "label": 5,
                },
                "hot_weather": {  # Label 8
                    "events": [
                        "cuaca panas",
                        "musim kemarau",
                        "hari yang terik",
                        "siang hari panas",
                        "cuaca terik",
                        "suasana panas",
                    ],
                    "responses": [
                        "kenakan pakaian berbahan katun yang menyerap keringat",
                        "padukan kaos lengan pendek dengan celana pendek",
                        "gunakan baju berbahan ringan dan breathable",
                        "pilih pakaian berwarna cerah dan berbahan ringan",
                    ],
                    "label": 8,
                },
                "cold_weather": {  # Label 9
                    "events": [
                        "cuaca dingin",
                        "musim hujan",
                        "suhu dingin",
                        "cuaca sejuk",
                        "musim dingin",
                        "suasana dingin",
                    ],
                    "responses": [
                        "kenakan sweater tebal dengan celana panjang",
                        "padukan jaket tebal dengan syal dan boots",
                        "gunakan pakaian berlapis dengan mantel hangat",
                        "kombinasikan sweater rajut dengan celana wool",
                    ],
                    "label": 9,
                },
                "rainy_weather": {  # Label 10
                    "events": [
                        "hujan",
                        "cuaca hujan",
                        "musim hujan",
                        "hari hujan",
                        "hujan deras",
                        "gerimis",
                    ],
                    "responses": [
                        "kenakan jas hujan dengan sepatu anti air",
                        "padukan jaket waterproof dengan celana panjang dan boots",
                        "gunakan pakaian yang cepat kering dengan sepatu boots anti air",
                        "kombinasikan raincoat dengan celana panjang dan sepatu tahan air",
                    ],
                    "label": 10,
                },
                "windy_weather": {  # Label 11
                    "events": [
                        "cuaca berangin",
                        "angin kencang",
                        "musim angin",
                        "hari berangin",
                    ],
                    "responses": [
                        "kenakan jaket windbreaker dengan celana panjang",
                        "padukan sweater dengan celana yang pas dan tidak berkibar",
                        "gunakan pakaian berlapis dengan jaket tahan angin",
                        "kombinasikan jaket dengan celana yang nyaman dan tidak longgar",
                    ],
                    "label": 11,
                },
                "spring": {  # Label 14
                    "events": [
                        "musim semi",
                        "awal musim semi",
                        "suasana semi",
                        "cuaca semi",
                    ],
                    "responses": [
                        "kenakan dress floral dengan cardigan ringan",
                        "padukan kemeja tipis dengan celana chino",
                        "gunakan pakaian berlapis yang mudah dilepas",
                        "kombinasikan blus dengan rok midi dan flat shoes",
                    ],
                    "label": 14,
                },
                "autumn": {  # Label 15
                    "events": [
                        "musim gugur",
                        "awal musim gugur",
                        "suasana gugur",
                        "cuaca gugur",
                    ],
                    "responses": [
                        "kenakan sweater rajut dengan celana panjang",
                        "padukan jaket kulit dengan jeans dan boots",
                        "gunakan pakaian berlapis dengan warna earth tone",
                        "kombinasikan turtleneck dengan coat ringan",
                    ],
                    "label": 15,
                },
            },
        }

    def generate_dataset(self, samples_per_category: int = 100) -> pd.DataFrame:
        dataset = []

        for occasion_type, details in self.templates["occasions"].items():
            for _ in range(samples_per_category):
                event = random.choice(details["events"])
                template = random.choice(self.templates["query_templates"])
                response = random.choice(details["responses"])

                query = template.format(occasion=event)

                dataset.append(
                    {
                        "query": query,
                        "response": f"Untuk {event}, {response}",
                        "label": details["label"],
                    }
                )

                if random.random() < 0.3:
                    words = query.split()
                    if len(words) > 3:
                        random.shuffle(words[1:-1])
                        variant_query = " ".join(words)
                        dataset.append(
                            {
                                "query": variant_query,
                                "response": f"Untuk {event}, {response}",
                                "label": details["label"],
                            }
                        )

        return pd.DataFrame(dataset)


def combine_with_original_dataset():
    original_df = pd.read_csv("train/dataset.csv")
    print(f"Original dataset size: {len(original_df)}")

    generator = FashionDatasetGenerator()
    generated_df = generator.generate_dataset(samples_per_category=100)
    print(f"Generated dataset size: {len(generated_df)}")

    combined_df = pd.concat([original_df, generated_df], ignore_index=True)

    combined_df = combined_df.drop_duplicates(subset=["query"])
    print(f"Combined dataset size after removing duplicates: {len(combined_df)}")

    os.makedirs("data/processed", exist_ok=True)
    combined_df.to_csv("data/processed/combined_dataset.csv", index=False)
    print("Combined dataset saved to data/processed/combined_dataset.csv")

    print("\nLabel distribution in combined dataset:")
    label_counts = combined_df["label"].value_counts().sort_index()
    for label, count in label_counts.items():
        print(f"Label {label}: {count} examples")


if __name__ == "__main__":
    combine_with_original_dataset()
