# src/update_metadata_entries.py
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


def update_metadata_with_all_files(metadata_file, audio_root_dir):
    """Update metadata to include all WAV files in the audio directory."""
    try:
        # Read existing metadata if it exists
        if os.path.exists(metadata_file):
            df = pd.read_csv(metadata_file)
            print(f"Loaded existing metadata with {len(df)} entries")
        else:
            # Create new metadata DataFrame with required columns
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
            print("Created new metadata file")

        # Get list of existing filenames in metadata
        existing_files = set(df["filename"]) if not df.empty else set()

        # Find all WAV files in the audio directory
        new_entries = []
        for root, _, files in os.walk(audio_root_dir):
            for filename in files:
                if filename.endswith(".wav"):
                    # Get relative path from audio_root_dir
                    rel_path = os.path.relpath(
                        os.path.join(root, filename), audio_root_dir
                    )

                    # Skip if file already in metadata
                    if rel_path in existing_files:
                        continue

                    # Get file properties
                    filepath = os.path.join(root, filename)
                    duration = get_audio_duration(filepath)

                    # Determine category from path
                    category = os.path.basename(os.path.dirname(filepath))

                    # Create default entry (user can update expected_text later)
                    entry = {
                        "filename": rel_path,
                        "expected_text": "[FILL IN THE TEXT]",  # Placeholder
                        "category": category,
                        "duration_seconds": duration,
                        "background_noise": "none",
                        "accent": "standard",
                        "speaking_speed": "normal",
                        "eq_profile": "neutral",
                        "distance": "medium",
                    }

                    # Try to extract properties from filename
                    base_filename = os.path.basename(filename)
                    if "_" in base_filename:
                        parts = base_filename.replace(".wav", "").split("_")
                        if len(parts) >= 2:
                            # For filenames like "speed_fast_formal.wav"
                            if parts[0] == "speed":
                                entry["speaking_speed"] = parts[1]
                            elif parts[0] == "accent":
                                entry["accent"] = parts[1]
                            elif parts[0] == "noise":
                                entry["background_noise"] = parts[1]
                            elif parts[0] == "eq":
                                entry["eq_profile"] = parts[1]
                            elif parts[0] == "distance":
                                entry["distance"] = parts[1]

                    new_entries.append(entry)

        # Add new entries to the DataFrame
        if new_entries:
            new_df = pd.DataFrame(new_entries)
            df = pd.concat([df, new_df], ignore_index=True)
            print(f"Added {len(new_entries)} new entries")
        else:
            print("No new files found")

        # Save updated metadata
        df.to_csv(metadata_file, index=False)
        print(f"Saved metadata with {len(df)} total entries to {metadata_file}")

        # Show files with placeholder text
        placeholders = df[df["expected_text"] == "[FILL IN THE TEXT]"]
        if not placeholders.empty:
            print("\nThe following files need expected text to be filled in:")
            for _, row in placeholders.iterrows():
                print(f"- {row['filename']}")

    except Exception as e:
        print(f"Error updating metadata: {str(e)}")


if __name__ == "__main__":
    metadata_file = "test_data/audio_metadata.csv"
    audio_root_dir = "test_data/audio_samples"

    update_metadata_with_all_files(metadata_file, audio_root_dir)
