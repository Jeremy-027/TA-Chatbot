# Save as src/tests/update_real_world_metadata.py
import os
import pandas as pd
import wave


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

                # Get relative path from audio_samples dir
                rel_path = os.path.join("real_world", filename)

                # Check if file already in metadata
                if rel_path in df["filename"].values:
                    print(f"File already in metadata: {rel_path}")
                    continue

                # Get duration
                duration = get_audio_duration(filepath)

                # Create entry with placeholder text
                entry = {
                    "filename": rel_path,
                    "expected_text": "[FILL IN THE TEXT]",  # You'll edit this manually later
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

            print(
                "\nPlease edit the CSV file to replace [FILL IN THE TEXT] with the actual spoken text."
            )

    except Exception as e:
        print(f"Error updating metadata: {str(e)}")


if __name__ == "__main__":
    update_metadata_for_real_world_tests()
