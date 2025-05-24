# src/tests/create_test_datasets.py
import pandas as pd
import os
import random


def create_nlp_test_cases():
    """Create NLP test cases with various phrasings and dialects."""
    test_cases = []

    # Standard queries
    test_cases.extend(
        [
            {"query": "saya mencari baju formal untuk interview", "expected_intent": 0},
            {
                "query": "rekomendasi pakaian untuk wanita berkulit sawo matang",
                "expected_intent": 3,
            },
            {"query": "outfit casual untuk hang out", "expected_intent": 4},
            {"query": "pakaian yang cocok untuk cuaca panas", "expected_intent": 11},
            {"query": "baju untuk musim dingin", "expected_intent": 16},
        ]
    )

    # Language variations
    test_cases.extend(
        [
            # Dialects/colloquialisms
            {"query": "mo cari baju formal buat interview dong", "expected_intent": 0},
            {
                "query": "mau ngecek baju apa yang cocok buat ke kantor",
                "expected_intent": 0,
            },
            {"query": "outfit santai buat nongkrong di café", "expected_intent": 4},
            # Abbreviated forms
            {"query": "baju interview", "expected_intent": 0},
            {"query": "fashion panas", "expected_intent": 11},
            # Mixed Indonesian and English
            {"query": "outfit yang bagus untuk office meeting", "expected_intent": 10},
            {"query": "dress code untuk wedding", "expected_intent": 8},
            # Different word orders
            {
                "query": "untuk interview kerja baju apa yang cocok",
                "expected_intent": 0,
            },
            {
                "query": "berkulit sawo matang, wanita, pakaian formal",
                "expected_intent": 3,
            },
        ]
    )

    # Add more test cases to cover various aspects

    # Create and save dataframe
    df = pd.DataFrame(test_cases)
    os.makedirs("test_data", exist_ok=True)
    df.to_csv("test_data/nlp_test_cases.csv", index=False)
    print(f"Created {len(df)} NLP test cases")


def create_language_variations():
    """Create groups of language variations for the same intent."""
    variations = []

    # Formal wear variations
    formal_variations = [
        {"query": "baju formal untuk interview", "variation_group": "formal_interview"},
        {
            "query": "pakaian untuk meeting kantor",
            "variation_group": "formal_interview",
        },
        {
            "query": "outfit untuk presentasi bisnis",
            "variation_group": "formal_interview",
        },
        {"query": "busana untuk acara formal", "variation_group": "formal_interview"},
        {"query": "setelan untuk rapat penting", "variation_group": "formal_interview"},
    ]
    variations.extend(formal_variations)

    # Casual wear variations
    casual_variations = [
        {"query": "baju santai untuk jalan-jalan", "variation_group": "casual_outing"},
        {"query": "outfit untuk nongkrong", "variation_group": "casual_outing"},
        {"query": "pakaian buat hangout", "variation_group": "casual_outing"},
        {"query": "busana untuk main ke mall", "variation_group": "casual_outing"},
        {"query": "fashion untuk santai di café", "variation_group": "casual_outing"},
    ]
    variations.extend(casual_variations)

    # Weather-related variations
    weather_variations = [
        {"query": "baju untuk cuaca panas", "variation_group": "hot_weather"},
        {"query": "pakaian saat terik", "variation_group": "hot_weather"},
        {"query": "outfit untuk hari yang gerah", "variation_group": "hot_weather"},
        {"query": "busana untuk musim kemarau", "variation_group": "hot_weather"},
        {"query": "fashion untuk iklim tropis", "variation_group": "hot_weather"},
    ]
    variations.extend(weather_variations)

    # Add more variation groups

    # Create and save dataframe
    df = pd.DataFrame(variations)
    df.to_csv("test_data/language_variations.csv", index=False)
    print(
        f"Created {len(df)} language variations in {len(df['variation_group'].unique())} groups"
    )


if __name__ == "__main__":
    create_nlp_test_cases()
    create_language_variations()

    # Note: For speech recognition test data, you would need to create audio files
    # with recorded Indonesian speech samples matching the transcripts in the test cases
