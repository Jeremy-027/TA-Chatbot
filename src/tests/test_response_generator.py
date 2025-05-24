# src/tests/test_response_generator.py
import os
import sys
import json
import time
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

# Add the parent directory to the path so we can import from src
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import the response generator
from response_generator import ResponseGenerator
from clothing_selector import generate_clothing_selection


def create_test_scenarios():
    """Create diverse test scenarios for response generation."""
    scenarios = [
        # Format: (scenario_name, parameters)
        # Formal scenarios
        (
            "formal_male_light",
            {"gender": "pria", "skin_tone": "light", "occasion": "formal"},
        ),
        (
            "formal_female_light",
            {"gender": "wanita", "skin_tone": "light", "occasion": "formal"},
        ),
        (
            "formal_male_dark",
            {"gender": "pria", "skin_tone": "dark", "occasion": "formal"},
        ),
        (
            "formal_female_dark",
            {"gender": "wanita", "skin_tone": "dark", "occasion": "formal"},
        ),
        # Casual scenarios
        (
            "casual_male_light",
            {"gender": "pria", "skin_tone": "light", "occasion": "casual"},
        ),
        (
            "casual_female_light",
            {"gender": "wanita", "skin_tone": "light", "occasion": "casual"},
        ),
        (
            "casual_male_dark",
            {"gender": "pria", "skin_tone": "dark", "occasion": "casual"},
        ),
        (
            "casual_female_dark",
            {"gender": "wanita", "skin_tone": "dark", "occasion": "casual"},
        ),
        # Special occasions
        (
            "wedding",
            {"gender": "neutral", "skin_tone": "neutral", "occasion": "wedding"},
        ),
        ("party", {"gender": "neutral", "skin_tone": "neutral", "occasion": "party"}),
        (
            "business_meeting",
            {
                "gender": "neutral",
                "skin_tone": "neutral",
                "occasion": "business_meeting",
            },
        ),
        # Weather-based scenarios
        (
            "hot_weather",
            {"gender": "neutral", "skin_tone": "neutral", "weather": "hot"},
        ),
        (
            "cold_weather",
            {"gender": "neutral", "skin_tone": "neutral", "weather": "cold"},
        ),
        (
            "rainy_weather",
            {"gender": "neutral", "skin_tone": "neutral", "weather": "rainy"},
        ),
        (
            "windy_weather",
            {"gender": "neutral", "skin_tone": "neutral", "weather": "windy"},
        ),
        # Season-based scenarios
        ("summer", {"gender": "neutral", "skin_tone": "neutral", "season": "summer"}),
        ("winter", {"gender": "neutral", "skin_tone": "neutral", "season": "winter"}),
        ("spring", {"gender": "neutral", "skin_tone": "neutral", "season": "spring"}),
        ("autumn", {"gender": "neutral", "skin_tone": "neutral", "season": "autumn"}),
        # Mixed scenarios (more complex)
        (
            "formal_male_light_cold",
            {
                "gender": "pria",
                "skin_tone": "light",
                "occasion": "formal",
                "weather": "cold",
            },
        ),
        (
            "casual_female_dark_hot",
            {
                "gender": "wanita",
                "skin_tone": "dark",
                "occasion": "casual",
                "weather": "hot",
            },
        ),
        (
            "wedding_summer",
            {
                "gender": "neutral",
                "skin_tone": "neutral",
                "occasion": "wedding",
                "season": "summer",
            },
        ),
        (
            "business_meeting_rainy",
            {
                "gender": "neutral",
                "skin_tone": "neutral",
                "occasion": "business_meeting",
                "weather": "rainy",
            },
        ),
    ]

    return scenarios


def test_response_generator():
    """Test the response generator with various scenarios."""
    try:
        # Create results directory
        results_dir = "test_results"
        os.makedirs(results_dir, exist_ok=True)

        # Initialize response generator
        print("Initializing Response Generator...")
        response_gen = ResponseGenerator()

        # Get test scenarios
        scenarios = create_test_scenarios()
        print(f"Created {len(scenarios)} test scenarios")

        # Test each scenario
        results = []
        for scenario_name, parameters in scenarios:
            print(f"Testing scenario: {scenario_name}")

            # Measure response time
            start_time = time.time()
            text_response, json_response = response_gen.generate_response(parameters)
            end_time = time.time()
            processing_time = end_time - start_time

            # Parse JSON response
            try:
                json_data = (
                    json.loads(json_response)
                    if isinstance(json_response, str)
                    else json_response
                )
                json_ok = True
            except:
                json_data = {}
                json_ok = False

            # Analyze response properties
            response_length = len(text_response) if text_response else 0
            has_recommendation = (
                "pakai" in text_response.lower() or "kenakan" in text_response.lower()
            )
            has_color_advice = any(
                color in text_response.lower()
                for color in [
                    "merah",
                    "biru",
                    "hijau",
                    "kuning",
                    "pink",
                    "ungu",
                    "orange",
                    "hitam",
                    "putih",
                    "coklat",
                    "abu-abu",
                ]
            )

            # Validate JSON response for 3D visualization
            if json_ok:
                has_clothing = "clothing" in json_data
                clothing_items = len(json_data.get("clothing", {}))
                has_parameters = "parameters" in json_data
            else:
                has_clothing = False
                clothing_items = 0
                has_parameters = False

            # Store result
            result = {
                "scenario": scenario_name,
                "parameters": str(parameters),
                "response_length": response_length,
                "processing_time": processing_time,
                "has_recommendation": has_recommendation,
                "has_color_advice": has_color_advice,
                "json_valid": json_ok,
                "has_clothing_items": has_clothing,
                "clothing_item_count": clothing_items,
                "has_parameters": has_parameters,
                "text_response": (
                    text_response[:100] + "..."
                    if len(text_response) > 100
                    else text_response
                ),
            }
            results.append(result)

        # Create results DataFrame
        results_df = pd.DataFrame(results)

        # Calculate statistics
        avg_processing_time = results_df["processing_time"].mean()
        pct_with_recommendation = results_df["has_recommendation"].mean() * 100
        pct_with_color_advice = results_df["has_color_advice"].mean() * 100
        pct_valid_json = results_df["json_valid"].mean() * 100

        # Create visualizations
        plt.figure(figsize=(12, 8))
        plt.bar(results_df["scenario"], results_df["processing_time"])
        plt.xlabel("Scenario")
        plt.ylabel("Processing Time (seconds)")
        plt.title("Response Generation Processing Time by Scenario")
        plt.xticks(rotation=90)
        plt.tight_layout()

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save processing time plot
        plot_file = os.path.join(results_dir, f"response_gen_times_{timestamp}.png")
        plt.savefig(plot_file)
        plt.close()

        # Save detailed results
        results_file = os.path.join(
            results_dir, f"response_gen_results_{timestamp}.csv"
        )
        results_df.to_csv(results_file, index=False)

        # Create summary
        summary = {
            "timestamp": timestamp,
            "total_scenarios": len(results),
            "average_processing_time": avg_processing_time,
            "percent_with_recommendation": pct_with_recommendation,
            "percent_with_color_advice": pct_with_color_advice,
            "percent_valid_json": pct_valid_json,
            "scenario_stats": {
                scenario: {
                    "processing_time": float(
                        results_df[results_df["scenario"] == scenario][
                            "processing_time"
                        ].values[0]
                    ),
                    "response_length": int(
                        results_df[results_df["scenario"] == scenario][
                            "response_length"
                        ].values[0]
                    ),
                    "json_valid": bool(
                        results_df[results_df["scenario"] == scenario][
                            "json_valid"
                        ].values[0]
                    ),
                }
                for scenario, _ in scenarios
            },
        }

        # Save summary
        summary_file = os.path.join(
            results_dir, f"response_gen_summary_{timestamp}.json"
        )
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        # Print summary
        print("\n" + "=" * 60)
        print(f"Response Generator Test Summary:")
        print("-" * 60)
        print(f"Total Scenarios: {len(results)}")
        print(f"Average Processing Time: {avg_processing_time:.4f} seconds")
        print(f"Responses with Recommendations: {pct_with_recommendation:.2f}%")
        print(f"Responses with Color Advice: {pct_with_color_advice:.2f}%")
        print(f"Valid JSON Responses: {pct_valid_json:.2f}%")
        print("=" * 60)
        print(f"Detailed results saved to: {results_file}")
        print(f"Summary saved to: {summary_file}")
        print(f"Processing time plot saved to: {plot_file}")

        return summary, results_df

    except Exception as e:
        print(f"Error in response generator testing: {str(e)}")
        import traceback

        traceback.print_exc()
        return None, None


if __name__ == "__main__":
    test_response_generator()
