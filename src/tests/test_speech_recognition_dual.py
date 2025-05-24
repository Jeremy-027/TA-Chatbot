# src/tests/test_speech_recognition_dual.py
import os
import pandas as pd
import json
import time
from datetime import datetime
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv


def setup_azure_speech():
    """Set up Azure Speech SDK with credentials from .env file."""
    # Same setup code as before
    # ...


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

        # Test each file and collect results
        # ...rest of testing code remains similar

        # Generate separate summaries for each test type
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = os.path.join(
            results_dir, f"speech_test_{test_type}_summary_{timestamp}.json"
        )

        # Return summary and results
        return summary, results_df

    except Exception as e:
        print(f"Error running tests: {str(e)}")
        raise


def compare_test_results():
    """Compare extreme vs real-world test results for comprehensive analysis."""
    # Run both test types
    extreme_summary, _ = test_speech_recognition("extreme")
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
