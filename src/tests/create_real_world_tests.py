# src/tests/create_real_world_tests.py
import os
import pandas as pd
import wave


def create_real_world_test_directory():
    """Create directory for real-world test files."""
    real_world_dir = "test_data/audio_samples/real_world"
    os.makedirs(real_world_dir, exist_ok=True)
    return real_world_dir


def get_audio_duration(filepath):
    """Get the duration of an audio file in seconds."""
    try:
        with wave.open(filepath, "rb") as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            duration = frames / float(rate)
            return round(duration, 1)
    except Exception as e:
        print(f"Error getting duration for {filepath}: {str(e)}")
        return 0.0


def update_metadata_for_real_world_tests():
    """Update the metadata file with real-world test entries."""
    metadata_file = "test_data/audio_metadata.csv"

    try:
        # Load existing metadata
        if os.path.exists(metadata_file):
            df = pd.read_csv(metadata_file)
        else:
            df = pd.DataFrame(
                columns=[
                    "filename",
                    "expected_text",
                    "category",
                    "duration_seconds",
                    "background_noise",
                    "accent",
                    "speaking_speed",
                    "eq_profile",
                    "distance",
                ]
            )

        # Get real-world test files
        real_world_dir = "test_data/audio_samples/real_world"
        new_entries = []

        for filename in os.listdir(real_world_dir):
            if filename.endswith(".wav"):
                filepath = os.path.join(real_world_dir, filename)

                # Get relative path
                rel_path = os.path.join("real_world", filename)

                # Skip if file already in metadata
                if rel_path in df["filename"].values:
                    continue

                # Get duration
                duration = get_audio_duration(filepath)

                # Create entry (with placeholder text)
                entry = {
                    "filename": rel_path,
                    "expected_text": "[FILL IN THE TEXT]",  # Need to update manually
                    "category": "real_world",
                    "duration_seconds": duration,
                    "background_noise": "minimal",
                    "accent": "standard",
                    "speaking_speed": "normal",
                    "eq_profile": "neutral",
                    "distance": "optimal",
                }

                new_entries.append(entry)

        # Add new entries
        if new_entries:
            new_df = pd.DataFrame(new_entries)
            df = pd.concat([df, new_df], ignore_index=True)
            print(f"Added {len(new_entries)} new real-world test entries")
        else:
            print("No new real-world test files found")

        # Save updated metadata
        df.to_csv(metadata_file, index=False)
        print(f"Metadata updated with real-world tests")

        # Show files with placeholder text
        placeholders = df[df["expected_text"] == "[FILL IN THE TEXT]"]
        if not placeholders.empty:
            print("\nThe following files need expected text to be filled in:")
            for _, row in placeholders.iterrows():
                print(f"- {row['filename']}")

    except Exception as e:
        print(f"Error updating metadata: {str(e)}")


def suggest_real_world_test_scenarios():
    """Suggest real-world test scenarios to record."""
    scenarios = [
        (
            "rw_formal_query.wav",
            "Saya mencari baju formal untuk interview kerja",
            "Standard query for formal wear",
        ),
        (
            "rw_casual_query.wav",
            "Rekomendasi pakaian casual untuk jalan-jalan",
            "Standard query for casual wear",
        ),
        (
            "rw_weather_query.wav",
            "Baju apa yang cocok untuk cuaca panas",
            "Weather-related fashion query",
        ),
        (
            "rw_wedding_query.wav",
            "Outfit untuk ke pesta pernikahan teman",
            "Special occasion query",
        ),
        (
            "rw_color_query.wav",
            "Warna apa yang bagus untuk kulit sawo matang",
            "Color recommendation query",
        ),
        (
            "rw_male_formal.wav",
            "Saya pria mau ke interview kerja, sebaiknya pakai apa",
            "Gender-specific formal query",
        ),
        (
            "rw_female_casual.wav",
            "Pakaian santai untuk wanita berkulit cerah",
            "Gender and skin tone casual query",
        ),
        (
            "rw_season_query.wav",
            "Baju yang cocok untuk musim hujan",
            "Seasonal fashion query",
        ),
        (
            "rw_accessory_query.wav",
            "Aksesoris apa yang cocok dengan kemeja putih",
            "Accessory recommendation query",
        ),
        (
            "rw_work_query.wav",
            "Rekomendasi pakaian untuk ke kantor",
            "Work attire query",
        ),
        (
            "rw_trendy_query.wav",
            "Fashion yang sedang trend untuk pria",
            "Trend-focused query",
        ),
        (
            "rw_combination_query.wav",
            "Cara mix and match kemeja biru",
            "Style combination query",
        ),
    ]

    print("\nSuggested Real-World Test Scenarios to Record:")
    print("-" * 60)
    for filename, text, description in scenarios:
        print(f"Filename: {filename}")
        print(f'Text to Speak: "{text}"')
        print(f"Description: {description}")
        print("-" * 40)

    print(
        "\nRecord these in a quiet environment with clear speech at a comfortable distance."
    )
    print(
        "After recording, run update_metadata_for_real_world_tests() to update the metadata file."
    )


if __name__ == "__main__":
    create_real_world_test_directory()
    suggest_real_world_test_scenarios()

    answer = input("Have you recorded the real-world test files? (y/n): ")
    if answer.lower() == "y":
        update_metadata_for_real_world_tests()
    else:
        print(
            "Please record the real-world test files first, then run this script again."
        )
