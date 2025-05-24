# src/update_audio_metadata.py
import os
import csv
import wave
from pydub import AudioSegment
import pandas as pd


def get_audio_duration(filepath):
    """Get the duration of an audio file in seconds."""
    try:
        with wave.open(filepath, "rb") as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            duration = frames / float(rate)
            return round(duration, 1)
    except:
        try:
            # Try with pydub if wave module fails
            audio = AudioSegment.from_file(filepath)
            duration = len(audio) / 1000.0
            return round(duration, 1)
        except Exception as e:
            print(f"Error getting duration for {filepath}: {str(e)}")
            return 0.0


def update_metadata_durations(metadata_file, audio_root_dir):
    """Update the duration_seconds column in the metadata CSV file."""
    try:
        # Read existing metadata
        df = pd.read_csv(metadata_file)

        # Update durations
        for i, row in df.iterrows():
            filepath = os.path.join(audio_root_dir, row["filename"])

            if os.path.exists(filepath):
                duration = get_audio_duration(filepath)
                df.at[i, "duration_seconds"] = duration
            else:
                print(f"Warning: File not found - {filepath}")

        # Save updated metadata
        df.to_csv(metadata_file, index=False)
        print(f"Updated durations in {metadata_file}")

    except Exception as e:
        print(f"Error updating metadata: {str(e)}")


if __name__ == "__main__":
    metadata_file = "test_data/audio_metadata.csv"
    audio_root_dir = "test_data/audio_samples"

    update_metadata_durations(metadata_file, audio_root_dir)
