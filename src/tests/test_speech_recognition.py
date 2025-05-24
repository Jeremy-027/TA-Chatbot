# src/test_speech_recognition.py
import os
import pandas as pd
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import time
import json
from datetime import datetime


def setup_azure_speech():
    """Set up the Azure Speech SDK with credentials from .env file."""
    load_dotenv()
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")

    if not speech_key or not speech_region:
        raise ValueError("Azure Speech credentials not found in .env file")

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key, region=speech_region
    )
    speech_config.speech_recognition_language = "id-ID"

    return speech_config


def calculate_word_error_rate(reference, hypothesis):
    """Calculate Word Error Rate between reference and hypothesis."""
    # Convert to lowercase and split into words
    reference_words = reference.lower().split()
    hypothesis_words = hypothesis.lower().split() if hypothesis else []

    # Calculate Levenshtein distance
    r_len = len(reference_words)
    h_len = len(hypothesis_words)

    # Initialize matrix with edit distances
    d = [[0 for _ in range(h_len + 1)] for _ in range(r_len + 1)]

    # Fill first row and column with edit distances
    for i in range(r_len + 1):
        d[i][0] = i
    for j in range(h_len + 1):
        d[0][j] = j

    # Calculate minimum edit distance
    for i in range(1, r_len + 1):
        for j in range(1, h_len + 1):
            if reference_words[i - 1] == hypothesis_words[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(
                    d[i - 1][j] + 1,  # deletion
                    d[i][j - 1] + 1,  # insertion
                    d[i - 1][j - 1] + 1,  # substitution
                )

    # Calculate WER
    distance = d[r_len][h_len]
    if r_len == 0:
        return 0.0

    return distance / r_len


def test_audio_file(speech_config, filepath, expected_text):
    """Test a single audio file with Azure Speech Recognition."""
    audio_config = speechsdk.audio.AudioConfig(filename=filepath)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    start_time = time.time()
    result = speech_recognizer.recognize_once()
    end_time = time.time()

    processing_time = end_time - start_time

    # Determine recognition status
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        recognized_text = result.text
        wer = calculate_word_error_rate(expected_text, recognized_text)
        is_success = wer < 0.5  # Consider it success if WER less than 50%
    else:
        recognized_text = ""
        wer = 1.0  # 100% error
        is_success = False

    return {
        "filepath": filepath,
        "expected_text": expected_text,
        "recognized_text": recognized_text,
        "wer": wer,
        "is_success": is_success,
        "processing_time": processing_time,
        "status": str(result.reason),
    }


def run_tests(metadata_file, audio_root_dir):
    """Run tests on all audio files in the metadata."""
    try:
        # Set up Azure Speech
        speech_config = setup_azure_speech()

        # Read metadata
        df = pd.read_csv(metadata_file)

        # Create results directory
        results_dir = "test_results"
        os.makedirs(results_dir, exist_ok=True)

        # Initialize results
        results = []

        # Test each file
        total_files = len(df)
        print(f"Starting tests on {total_files} files...")

        for i, row in df.iterrows():
            filepath = os.path.join(audio_root_dir, row["filename"])

            if not os.path.exists(filepath):
                print(f"Warning: File not found - {filepath}")
                continue

            print(f"Testing {i+1}/{total_files}: {row['filename']}")

            result = test_audio_file(speech_config, filepath, row["expected_text"])

            # Add metadata to result
            for col in df.columns:
                if col != "filename" and col != "expected_text":
                    result[col] = row[col]

            results.append(result)

            # Sleep briefly to avoid rate limiting
            time.sleep(0.5)

        # Create results dataframe
        results_df = pd.DataFrame(results)

        # Save detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = os.path.join(results_dir, f"speech_test_results_{timestamp}.csv")
        results_df.to_csv(results_file, index=False)

        # Generate summary statistics
        summary = {
            "timestamp": timestamp,
            "total_files": len(results),
            "successful_recognitions": sum(results_df["is_success"]),
            "success_rate": (
                sum(results_df["is_success"]) / len(results) if results else 0
            ),
            "average_wer": results_df["wer"].mean(),
            "average_processing_time": results_df["processing_time"].mean(),
            "category_results": {},
        }

        # Calculate category-specific results
        for category in results_df["category"].unique():
            category_df = results_df[results_df["category"] == category]
            summary["category_results"][category] = {
                "total": len(category_df),
                "success_rate": (
                    sum(category_df["is_success"]) / len(category_df)
                    if len(category_df) > 0
                    else 0
                ),
                "average_wer": category_df["wer"].mean(),
            }

        # Save summary
        summary_file = os.path.join(
            results_dir, f"speech_test_summary_{timestamp}.json"
        )
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        # Print summary
        print("\n" + "=" * 60)
        print(f"Test Summary:")
        print("-" * 60)
        print(f"Total Files: {summary['total_files']}")
        print(f"Successful Recognitions: {summary['successful_recognitions']}")
        print(f"Overall Success Rate: {summary['success_rate']:.2%}")
        print(f"Average Word Error Rate: {summary['average_wer']:.4f}")
        print(
            f"Average Processing Time: {summary['average_processing_time']:.4f} seconds"
        )
        print("\nCategory Results:")
        for category, results in summary["category_results"].items():
            print(
                f"  {category}: {results['success_rate']:.2%} success rate, {results['average_wer']:.4f} WER"
            )
        print("=" * 60)
        print(f"Detailed results saved to: {results_file}")
        print(f"Summary saved to: {summary_file}")

        return summary, results_df

    except Exception as e:
        print(f"Error running tests: {str(e)}")
        raise


if __name__ == "__main__":
    metadata_file = "test_data/audio_metadata.csv"
    audio_root_dir = "test_data/audio_samples"

    run_tests(metadata_file, audio_root_dir)
