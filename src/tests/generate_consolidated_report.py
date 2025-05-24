# src/tests/generate_consolidated_report.py
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def find_latest_test_files():
    """Find the latest test summary files for each test type."""
    results_dir = "test_results"

    # Define test types and their file prefixes
    test_types = {
        "speech": "speech_test_summary_",
        "nlp": "nlp_test_summary_",
        "response": "response_gen_summary_",
        "e2e": "e2e_test_summary_",
        "load": "load_test_summary_",
    }

    latest_files = {}

    # Find latest file for each test type
    for test_type, prefix in test_types.items():
        matching_files = [
            f
            for f in os.listdir(results_dir)
            if f.startswith(prefix) and f.endswith(".json")
        ]
        if matching_files:
            # Sort by timestamp in filename
            matching_files.sort(reverse=True)
            latest_files[test_type] = os.path.join(results_dir, matching_files[0])

    return latest_files


def generate_consolidated_report():
    """Generate a consolidated report from all test results."""
    # Find latest test files
    latest_files = find_latest_test_files()

    if not latest_files:
        print("No test results found.")
        return

    # Create results directory for the report
    report_dir = "test_reports"
    os.makedirs(report_dir, exist_ok=True)

    # Read test summaries
    summaries = {}
    for test_type, file_path in latest_files.items():
        try:
            with open(file_path, "r") as f:
                summaries[test_type] = json.load(f)
        except Exception as e:
            print(f"Error reading {test_type} summary: {str(e)}")

    # Generate timestamp for the report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create consolidated metrics
    consolidated_metrics = {
        "timestamp": timestamp,
        "speech_recognition": {
            "accuracy": (
                summaries.get("speech", {}).get("success_rate", 0) / 100
                if "speech" in summaries
                else None
            ),
            "average_wer": (
                summaries.get("speech", {}).get("average_wer", 0)
                if "speech" in summaries
                else None
            ),
            "processing_time": (
                summaries.get("speech", {}).get("average_processing_time", 0)
                if "speech" in summaries
                else None
            ),
        },
        "nlp_intent_classification": {
            "accuracy": (
                summaries.get("nlp", {}).get("accuracy", 0)
                if "nlp" in summaries
                else None
            ),
            "processing_time": (
                summaries.get("nlp", {}).get("average_processing_time", 0)
                if "nlp" in summaries
                else None
            ),
        },
        "response_generation": {
            "recommendation_rate": (
                summaries.get("response", {}).get("percent_with_recommendation", 0)
                / 100
                if "response" in summaries
                else None
            ),
            "json_validity": (
                summaries.get("response", {}).get("percent_valid_json", 0) / 100
                if "response" in summaries
                else None
            ),
            "processing_time": (
                summaries.get("response", {}).get("average_processing_time", 0)
                if "response" in summaries
                else None
            ),
        },
        "end_to_end": {
            "success_rate": (
                summaries.get("e2e", {}).get("success_rate", 0) / 100
                if "e2e" in summaries
                else None
            ),
            "total_processing_time": (
                summaries.get("e2e", {}).get("average_total_processing_time", 0)
                if "e2e" in summaries
                else None
            ),
        },
        "system_load": {
            "throughput": (
                summaries.get("load", {}).get("queries_per_second", 0)
                if "load" in summaries
                else None
            ),
            "success_rate": (
                summaries.get("load", {}).get("success_rate", 0) / 100
                if "load" in summaries
                else None
            ),
            "p95_processing_time": (
                summaries.get("load", {}).get("p95_processing_time", 0)
                if "load" in summaries
                else None
            ),
            "max_cpu_usage": (
                summaries.get("load", {}).get("max_cpu_usage", 0)
                if "load" in summaries
                else None
            ),
            "max_memory_usage": (
                summaries.get("load", {}).get("max_memory_usage_mb", 0)
                if "load" in summaries
                else None
            ),
        },
    }

    # Save consolidated metrics
    metrics_file = os.path.join(report_dir, f"consolidated_metrics_{timestamp}.json")
    with open(metrics_file, "w") as f:
        json.dump(consolidated_metrics, f, indent=2)

    # Create summary visualizations

    # Key Metrics Bar Chart
    plt.figure(figsize=(12, 8))

    metrics = [
        (
            "Speech Recognition\nAccuracy",
            consolidated_metrics["speech_recognition"]["accuracy"] or 0,
        ),
        (
            "NLP Intent\nAccuracy",
            consolidated_metrics["nlp_intent_classification"]["accuracy"] or 0,
        ),
        (
            "Response\nRecommendation Rate",
            consolidated_metrics["response_generation"]["recommendation_rate"] or 0,
        ),
        (
            "End-to-End\nSuccess Rate",
            consolidated_metrics["end_to_end"]["success_rate"] or 0,
        ),
        (
            "System Load\nSuccess Rate",
            consolidated_metrics["system_load"]["success_rate"] or 0,
        ),
    ]

    x_labels = [m[0] for m in metrics]
    values = [m[1] for m in metrics]

    plt.bar(x_labels, values)
    plt.ylim(0, 1.0)
    plt.ylabel("Success Rate")
    plt.title("Key Performance Metrics Across All Tests")

    # Add value labels on bars
    for i, v in enumerate(values):
        plt.text(i, v + 0.02, f"{v:.2%}", ha="center")

    plt.tight_layout()
    metrics_plot = os.path.join(report_dir, f"key_metrics_{timestamp}.png")
    plt.savefig(metrics_plot)
    plt.close()

    # Processing Time Comparison
    plt.figure(figsize=(10, 6))

    time_metrics = [
        (
            "Speech\nRecognition",
            consolidated_metrics["speech_recognition"]["processing_time"] or 0,
        ),
        (
            "NLP\nIntent",
            consolidated_metrics["nlp_intent_classification"]["processing_time"] or 0,
        ),
        (
            "Response\nGeneration",
            consolidated_metrics["response_generation"]["processing_time"] or 0,
        ),
        (
            "End-to-End\nTotal",
            consolidated_metrics["end_to_end"]["total_processing_time"] or 0,
        ),
        (
            "System Load\n(P95)",
            consolidated_metrics["system_load"]["p95_processing_time"] or 0,
        ),
    ]

    x_labels = [m[0] for m in time_metrics]
    values = [m[1] for m in time_metrics]

    plt.bar(x_labels, values)
    plt.ylabel("Processing Time (seconds)")
    plt.title("Processing Time Comparison Across Components")

    # Add value labels on bars
    for i, v in enumerate(values):
        plt.text(i, v + 0.05, f"{v:.2f}s", ha="center")

    plt.tight_layout()
    time_plot = os.path.join(report_dir, f"processing_times_{timestamp}.png")
    plt.savefig(time_plot)
    plt.close()

    # Generate HTML report
    html_report = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Fashion Chatbot Test Results</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1, h2, h3 {{ color: #2c3e50; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            .metric-card {{
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 15px;
                background-color: #f8f9fa;
            }}
            .metric-value {{
                font-size: 24px;
                font-weight: bold;
                color: #3498db;
                margin: 10px 0;
            }}
            .image-container {{ margin: 20px 0; }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #7f8c8d; }}
        </style>
    </head>
    <body>
        <h1>Indonesian Fashion Chatbot - Comprehensive Test Report</h1>
        <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

        <h2>Executive Summary</h2>
        <div class="metric-card">
            <h3>Overall System Performance</h3>
            <p>End-to-End Success Rate: <span class="metric-value">{consolidated_metrics["end_to_end"]["success_rate"]:.2%}</span></p>
            <p>Average Processing Time: <span class="metric-value">{consolidated_metrics["end_to_end"]["total_processing_time"]:.2f} seconds</span></p>
            <p>System Throughput: <span class="metric-value">{consolidated_metrics["system_load"]["throughput"]:.2f} queries/second</span></p>
        </div>

        <h2>Component Performance</h2>

        <div class="metric-card">
            <h3>Speech Recognition (Azure)</h3>
            <p>Recognition Accuracy: <span class="metric-value">{consolidated_metrics["speech_recognition"]["accuracy"]:.2%}</span></p>
            <p>Average Word Error Rate: <span class="metric-value">{consolidated_metrics["speech_recognition"]["average_wer"]:.4f}</span></p>
            <p>Average Processing Time: <span class="metric-value">{consolidated_metrics["speech_recognition"]["processing_time"]:.2f} seconds</span></p>
        </div>

        <div class="metric-card">
            <h3>NLP Intent Classification (IndoBERT)</h3>
            <p>Classification Accuracy: <span class="metric-value">{consolidated_metrics["nlp_intent_classification"]["accuracy"]:.2%}</span></p>
            <p>Average Processing Time: <span class="metric-value">{consolidated_metrics["nlp_intent_classification"]["processing_time"]:.2f} seconds</span></p>
        </div>

        <div class="metric-card">
            <h3>Response Generation</h3>
            <p>Recommendation Rate: <span class="metric-value">{consolidated_metrics["response_generation"]["recommendation_rate"]:.2%}</span></p>
            <p>JSON Validity Rate: <span class="metric-value">{consolidated_metrics["response_generation"]["json_validity"]:.2%}</span></p>
            <p>Average Processing Time: <span class="metric-value">{consolidated_metrics["response_generation"]["processing_time"]:.2f} seconds</span></p>
        </div>

        <div class="metric-card">
            <h3>System Load Performance</h3>
            <p>Success Rate Under Load: <span class="metric-value">{consolidated_metrics["system_load"]["success_rate"]:.2%}</span></p>
            <p>95th Percentile Processing Time: <span class="metric-value">{consolidated_metrics["system_load"]["p95_processing_time"]:.2f} seconds</span></p>
            <p>Maximum CPU Usage: <span class="metric-value">{consolidated_metrics["system_load"]["max_cpu_usage"]:.2f}%</span></p>
            <p>Maximum Memory Usage: <span class="metric-value">{consolidated_metrics["system_load"]["max_memory_usage"]:.2f} MB</span></p>
        </div>

        <h2>Visualizations</h2>

        <div class="image-container">
            <h3>Key Performance Metrics</h3>
            <img src="key_metrics_{timestamp}.png" alt="Key Performance Metrics" style="max-width: 100%;">
        </div>

        <div class="image-container">
            <h3>Processing Times Comparison</h3>
            <img src="processing_times_{timestamp}.png" alt="Processing Times Comparison" style="max-width: 100%;">
        </div>

        <h2>Recommendations</h2>
        <ul>
            <li><strong>Speech Recognition:</strong> {"Improve handling of accents and background noise" if consolidated_metrics["speech_recognition"]["accuracy"] < 0.8 else "Current performance is adequate, but consider ongoing monitoring"}</li>
            <li><strong>NLP Intent Classification:</strong> {"Consider model retraining or fine-tuning to improve accuracy" if consolidated_metrics["nlp_intent_classification"]["accuracy"] < 0.9 else "Model is performing well"}</li>
            <li><strong>Response Generation:</strong> {"Enhance recommendation quality and consistency" if consolidated_metrics["response_generation"]["recommendation_rate"] < 0.9 else "Recommendation system is working effectively"}</li>
            <li><strong>System Performance:</strong> {"Optimize for better throughput and response times" if consolidated_metrics["system_load"]["throughput"] < 2.0 else "Current system resources appear adequate"}</li>
        </ul>

        <div class="footer">
            <p>This report was automatically generated based on test results. For detailed analysis, please refer to the individual test result files.</p>
        </div>
    </body>
    </html>
    """

    # Save HTML report
    html_file = os.path.join(report_dir, f"consolidated_report_{timestamp}.html")
    with open(html_file, "w") as f:
        f.write(html_report)

    print("\n" + "=" * 60)
    print(f"Consolidated Report Generated:")
    print("-" * 60)
    print(f"Metrics saved to: {metrics_file}")
    print(f"Key metrics plot saved to: {metrics_plot}")
    print(f"Processing times plot saved to: {time_plot}")
    print(f"HTML report saved to: {html_file}")
    print("=" * 60)

    return html_file


if __name__ == "__main__":
    report_file = generate_consolidated_report()
    if report_file:
        print(f"Report generated successfully: {report_file}")
        # Try to open the report in a browser (works on many systems)
        import webbrowser

        webbrowser.open("file://" + os.path.abspath(report_file))
