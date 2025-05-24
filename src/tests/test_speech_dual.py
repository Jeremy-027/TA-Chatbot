# Save as src/tests/test_speech_dual.py
import os
import sys
import pandas as pd
import json
import time
from datetime import datetime
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv


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


def setup_azure_speech():
    """Set up Azure Speech SDK with credentials from .env file."""
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


def test_speech_recognition(test_type="all"):
    """
    Test speech recognition with option to test specific scenarios.

    Args:
        test_type (str): Type of test to run - "extreme", "real_world", or "all"
    """
    try:
        # Set up Azure Speech
        speech_config = setup_azure_speech()

        # Create results directory
        results_dir = "test_results"
        os.makedirs(results_dir, exist_ok=True)

        # Load test metadata
        metadata_file = "test_data/audio_metadata.csv"
        df = pd.read_csv(metadata_file)

        # Filter based on test type
        if test_type == "extreme":
            # Use the existing extreme test categories
            test_categories = ["accent", "speed", "noise", "edge", "eq", "distance"]
            test_df = df[df["category"].isin(test_categories)]
        elif test_type == "real_world":
            # Use only the real-world category
            test_df = df[df["category"] == "real_world"]
        else:  # "all"
            test_df = df

        print(f"Running {test_type} tests on {len(test_df)} audio files...")

        # Initialize results
        results = []
        audio_root_dir = "test_data/audio_samples"

        # Test each file
        for i, row in test_df.iterrows():
            filepath = os.path.join(audio_root_dir, row["filename"])

            if not os.path.exists(filepath):
                print(f"Warning: File not found - {filepath}")
                continue

            print(f"Testing {i+1}/{len(test_df)}: {row['filename']}")

            # Set up audio config
            audio_config = speechsdk.audio.AudioConfig(filename=filepath)
            speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config, audio_config=audio_config
            )

            # Recognize speech
            start_time = time.time()
            result = speech_recognizer.recognize_once()
            end_time = time.time()

            processing_time = end_time - start_time

            # Process result
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                recognized_text = result.text
                wer = calculate_word_error_rate(row["expected_text"], recognized_text)
                is_success = wer < 0.5  # Consider it success if WER less than 50%
            else:
                recognized_text = ""
                wer = 1.0  # 100% error
                is_success = False

            # Store result
            result_data = {
                "filename": row["filename"],
                "category": row["category"],
                "expected_text": row["expected_text"],
                "recognized_text": recognized_text,
                "wer": wer,
                "is_success": is_success,
                "processing_time": processing_time,
                "status": str(result.reason),
            }
            results.append(result_data)

            # Sleep briefly to avoid rate limiting
            time.sleep(0.5)

        # Create results dataframe
        results_df = pd.DataFrame(results)

        # Calculate statistics
        if len(results_df) > 0:
            success_rate = results_df["is_success"].mean()
            avg_wer = results_df["wer"].mean()
            avg_processing_time = results_df["processing_time"].mean()

            # Calculate category-specific results
            category_results = {}
            for category in results_df["category"].unique():
                category_df = results_df[results_df["category"] == category]
                category_results[category] = {
                    "total": len(category_df),
                    "success_rate": category_df["is_success"].mean(),
                    "average_wer": category_df["wer"].mean(),
                }
        else:
            success_rate = 0
            avg_wer = 0
            avg_processing_time = 0
            category_results = {}

        # Create summary
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary = {
            "timestamp": timestamp,
            "test_type": test_type,
            "total_files": len(results),
            "successful_recognitions": (
                sum(results_df["is_success"]) if len(results_df) > 0 else 0
            ),
            "success_rate": success_rate,
            "average_wer": avg_wer,
            "average_processing_time": avg_processing_time,
            "category_results": category_results,
        }

        # Save results
        results_file = os.path.join(
            results_dir, f"speech_test_{test_type}_results_{timestamp}.csv"
        )
        summary_file = os.path.join(
            results_dir, f"speech_test_{test_type}_summary_{timestamp}.json"
        )

        results_df.to_csv(results_file, index=False)
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        # Print summary
        print("\n" + "=" * 60)
        print(f"Speech Recognition Test Summary ({test_type}):")
        print("-" * 60)
        print(f"Total Files: {summary['total_files']}")
        print(f"Successful Recognitions: {summary['successful_recognitions']}")
        print(f"Success Rate: {summary['success_rate']:.2%}")
        print(f"Average Word Error Rate: {summary['average_wer']:.4f}")
        print(
            f"Average Processing Time: {summary['average_processing_time']:.4f} seconds"
        )

        if category_results:
            print("\nCategory Results:")
            for category, results in category_results.items():
                print(
                    f"  {category}: {results['success_rate']:.2%} success rate, {results['average_wer']:.4f} WER"
                )

        print("=" * 60)
        print(f"Detailed results saved to: {results_file}")
        print(f"Summary saved to: {summary_file}")

        return summary, results_df

    except Exception as e:
        print(f"Error running tests: {str(e)}")
        import traceback

        traceback.print_exc()
        return None, None


def compare_test_results():
    """Compare extreme vs real-world test results."""
    # Run both test types
    print("Running extreme tests...")
    extreme_summary, _ = test_speech_recognition("extreme")

    print("\nRunning real-world tests...")
    real_world_summary, _ = test_speech_recognition("real_world")

    # Create comparison report
    comparison = {
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "extreme_test": {
            "success_rate": extreme_summary["success_rate"],
            "average_wer": extreme_summary["average_wer"],
            "processing_time": extreme_summary["average_processing_time"],
        },
        "real_world_test": {
            "success_rate": real_world_summary["success_rate"],
            "average_wer": real_world_summary["average_wer"],
            "processing_time": real_world_summary["average_processing_time"],
        },
        "difference": {
            "success_rate_diff": real_world_summary["success_rate"]
            - extreme_summary["success_rate"],
            "wer_diff": extreme_summary["average_wer"]
            - real_world_summary["average_wer"],
        },
    }

    # Save comparison
    results_dir = "test_results"
    comparison_file = os.path.join(
        results_dir, f"speech_test_comparison_{comparison['timestamp']}.json"
    )
    with open(comparison_file, "w") as f:
        json.dump(comparison, f, indent=2)

    # Print comparison
    print("\n" + "=" * 60)
    print(f"Speech Recognition Test Comparison:")
    print("-" * 60)
    print(f"Extreme Test Success Rate: {extreme_summary['success_rate']:.2%}")
    print(f"Real-World Test Success Rate: {real_world_summary['success_rate']:.2%}")
    print(f"Difference: {comparison['difference']['success_rate_diff']:.2%}")
    print(f"Extreme Test WER: {extreme_summary['average_wer']:.4f}")
    print(f"Real-World Test WER: {real_world_summary['average_wer']:.4f}")
    print(f"Difference: {comparison['difference']['wer_diff']:.4f}")
    print("=" * 60)
    print(f"Comparison saved to: {comparison_file}")

    return comparison


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run speech recognition tests")
    parser.add_argument(
        "test_type",
        choices=["extreme", "real_world", "all", "compare"],
        help="Type of test to run",
    )

    args = parser.parse_args()

    if args.test_type == "compare":
        compare_test_results()
    else:
        test_speech_recognition(args.test_type)
