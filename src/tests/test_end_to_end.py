# src/tests/test_end_to_end.py
import os
import sys
import json
import time
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import traceback

# Add the parent directory to the path so we can import from src
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import required modules
from language_model import IndoBERTFashionProcessor


def create_test_queries():
    """Create diverse test queries for end-to-end testing."""
    test_queries = [
        # Basic queries
        ("Saya mencari baju formal untuk interview kerja", "formal_interview"),
        ("Rekomendasi pakaian casual untuk jalan-jalan", "casual_outing"),
        ("Outfit untuk ke pesta pernikahan", "wedding"),
        ("Baju yang cocok untuk cuaca panas", "hot_weather"),
        # Gender and skin tone specific
        ("Saya pria berkulit cerah, mau ke meeting kantor", "formal_male_light"),
        (
            "Outfit untuk wanita berkulit sawo matang ke acara casual",
            "casual_female_dark",
        ),
        ("Pakaian pria dengan kulit gelap untuk acara formal", "formal_male_dark"),
        ("Baju santai untuk cewek kulit putih", "casual_female_light"),
        # Complex queries with multiple parameters
        ("Baju formal pria untuk interview di musim dingin", "formal_male_winter"),
        (
            "Outfit wanita berkulit sawo matang untuk pesta saat cuaca panas",
            "party_female_dark_hot",
        ),
        (
            "Pakaian casual untuk pria berkulit cerah di musim hujan",
            "casual_male_light_rainy",
        ),
        (
            "Baju untuk wanita berkulit gelap ke meeting saat musim panas",
            "formal_female_dark_summer",
        ),
        # Ambiguous queries
        ("Bantu saya pilih baju", "general_help"),
        ("Outfit yang bagus", "general_recommendation"),
        ("Warna apa yang cocok untuk saya?", "color_recommendation"),
        ("Bagaimana cara mix and match baju?", "styling_advice"),
        # Multilingual queries
        ("Outfit casual yang trendy untuk hangout", "casual_trendy"),
        ("Baju formal yang professional looking", "formal_professional"),
        ("Fashion style untuk summer vacation", "summer_vacation"),
        ("Business attire untuk meeting penting", "business_meeting"),
        # Short queries
        ("Baju pesta?", "party_short"),
        ("Fashion formal?", "formal_short"),
        ("Outfit hujan?", "rainy_short"),
        ("Baju apa?", "general_short"),
        # Special occasions
        ("Baju untuk ke interview kerja pertama", "first_interview"),
        ("Outfit untuk dinner romantis", "romantic_dinner"),
        ("Pakaian untuk presentasi bisnis penting", "important_presentation"),
        ("Baju untuk travelling ke pantai", "beach_travel"),
    ]

    return test_queries


def test_end_to_end_pipeline(model_path="./fine-tuned-model"):
    """Test the end-to-end pipeline from query to response."""
    try:
        # Create results directory
        results_dir = "test_results"
        os.makedirs(results_dir, exist_ok=True)

        # Initialize the model
        print("Initializing IndoBERT model...")
        start_time = time.time()
        processor = IndoBERTFashionProcessor(model_path)
        model_load_time = time.time() - start_time
        print(f"Model loaded in {model_load_time:.2f} seconds")

        # Get test queries
        test_queries = create_test_queries()
        print(f"Created {len(test_queries)} test queries")

        # Test each query
        results = []
        for i, (query, query_type) in enumerate(test_queries):
            print(f"Testing query {i+1}/{len(test_queries)}: {query}")

            try:
                # Step 1: NLP Processing (Intent Classification)
                start_time_total = time.time()
                start_time_nlp = time.time()
                intent_id = processor.classify_intent(query)
                sentiment = processor.analyze_sentiment(query)
                nlp_time = time.time() - start_time_nlp

                # Step 2: Response Generation
                start_time_response = time.time()
                text_response, json_response = processor.generate_response(
                    query, intent_id, sentiment
                )
                response_time = time.time() - start_time_response

                total_time = time.time() - start_time_total

                # Analyze response
                success = text_response is not None and len(text_response) > 0

                # Try to parse JSON
                try:
                    if isinstance(json_response, str):
                        json_data = json.loads(json_response)
                    else:
                        json_data = json_response
                    json_valid = True
                except:
                    json_data = {}
                    json_valid = False

                # Store result
                result = {
                    "query": query,
                    "query_type": query_type,
                    "intent_id": intent_id,
                    "nlp_processing_time": nlp_time,
                    "response_generation_time": response_time,
                    "total_processing_time": total_time,
                    "success": success,
                    "json_valid": json_valid,
                    "response_length": len(text_response) if text_response else 0,
                    "response_preview": (
                        text_response[:100] + "..."
                        if text_response and len(text_response) > 100
                        else text_response
                    ),
                }
                results.append(result)

            except Exception as e:
                print(f"Error processing query: {query}")
                print(f"Error: {str(e)}")
                traceback.print_exc()

                result = {
                    "query": query,
                    "query_type": query_type,
                    "intent_id": -1,
                    "nlp_processing_time": 0,
                    "response_generation_time": 0,
                    "total_processing_time": 0,
                    "success": False,
                    "json_valid": False,
                    "response_length": 0,
                    "response_preview": f"ERROR: {str(e)}",
                }
                results.append(result)

        # Create results DataFrame
        results_df = pd.DataFrame(results)

        # Calculate statistics
        success_rate = results_df["success"].mean() * 100
        avg_total_time = results_df["total_processing_time"].mean()
        avg_nlp_time = results_df["nlp_processing_time"].mean()
        avg_response_time = results_df["response_generation_time"].mean()
        pct_json_valid = results_df["json_valid"].mean() * 100

        # Create visualization for processing times
        plt.figure(figsize=(14, 8))

        # Stacked bar chart of processing times
        indices = np.arange(len(results_df))
        width = 0.8

        nlp_times = results_df["nlp_processing_time"]
        response_times = results_df["response_generation_time"]

        plt.bar(indices, nlp_times, width, label="NLP Processing Time")
        plt.bar(
            indices,
            response_times,
            width,
            bottom=nlp_times,
            label="Response Generation Time",
        )

        plt.xlabel("Query Index")
        plt.ylabel("Processing Time (seconds)")
        plt.title("End-to-End Processing Time Breakdown")
        plt.xticks(indices, rotation=90)
        plt.legend()
        plt.tight_layout()

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save processing time plot
        plot_file = os.path.join(results_dir, f"e2e_processing_times_{timestamp}.png")
        plt.savefig(plot_file)
        plt.close()

        # Save detailed results
        results_file = os.path.join(results_dir, f"e2e_test_results_{timestamp}.csv")
        results_df.to_csv(results_file, index=False)

        # Create summary
        summary = {
            "timestamp": timestamp,
            "total_queries": len(results),
            "success_rate": success_rate,
            "average_total_processing_time": avg_total_time,
            "average_nlp_processing_time": avg_nlp_time,
            "average_response_generation_time": avg_response_time,
            "percent_valid_json": pct_json_valid,
            "model_load_time": model_load_time,
        }

        # Save summary
        summary_file = os.path.join(results_dir, f"e2e_test_summary_{timestamp}.json")
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        # Print summary
        print("\n" + "=" * 60)
        print(f"End-to-End Pipeline Test Summary:")
        print("-" * 60)
        print(f"Total Queries: {len(results)}")
        print(f"Success Rate: {success_rate:.2f}%")
        print(f"Average Total Processing Time: {avg_total_time:.4f} seconds")
        print(f"Average NLP Processing Time: {avg_nlp_time:.4f} seconds")
        print(f"Average Response Generation Time: {avg_response_time:.4f} seconds")
        print(f"Valid JSON Responses: {pct_json_valid:.2f}%")
        print(f"Model Load Time: {model_load_time:.2f} seconds")
        print("=" * 60)
        print(f"Detailed results saved to: {results_file}")
        print(f"Summary saved to: {summary_file}")
        print(f"Processing time plot saved to: {plot_file}")

        return summary, results_df

    except Exception as e:
        print(f"Error in end-to-end testing: {str(e)}")
        traceback.print_exc()
        return None, None


if __name__ == "__main__":
    test_end_to_end_pipeline()
