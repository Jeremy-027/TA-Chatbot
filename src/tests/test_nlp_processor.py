import os
import sys
import pandas as pd
import json
import time
from datetime import datetime
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Add the parent directory to the path so we can import from src
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Now import the language_model module
from language_model import IndoBERTFashionProcessor


def create_test_data():
    """Create test data for NLP intent classification."""
    # Define test cases for different intents
    test_cases = [
        # Format: (query, expected_intent_id)
        # Formal - Male - Light Skin
        ("Saya mencari baju formal untuk interview kerja", 0),
        ("Rekomendasi pakaian formal untuk pria berkulit cerah", 0),
        ("Baju apa yang cocok untuk pria dengan kulit putih ke acara formal?", 0),
        ("Outfit formal untuk laki-laki dengan kulit terang", 0),
        ("Pakaian kantor untuk cowok berkulit cerah", 0),
        # Formal - Female - Light Skin
        ("Saya wanita berkulit cerah, mau ke interview", 1),
        ("Rekomendasi baju formal untuk perempuan kulit putih", 1),
        ("Pakaian kerja untuk wanita kulit cerah", 1),
        ("Baju formal apa yang cocok untuk cewek berkulit terang?", 1),
        ("Outfit kantor untuk wanita dengan kulit putih", 1),
        # Formal - Male - Dark Skin
        ("Baju formal untuk pria berkulit sawo matang", 2),
        ("Pakaian kerja untuk laki-laki dengan kulit gelap", 2),
        ("Rekomendasi outfit formal pria kulit coklat", 2),
        ("Saya pria berkulit gelap mau ke interview", 2),
        ("Baju kantor untuk cowok sawo matang", 2),
        # Formal - Female - Dark Skin
        ("Pakaian formal untuk wanita berkulit sawo matang", 3),
        ("Baju kerja untuk perempuan kulit gelap", 3),
        ("Rekomendasi outfit formal untuk cewek berkulit coklat", 3),
        ("Saya wanita dengan kulit gelap, mau ke meeting", 3),
        ("Baju kantor untuk wanita sawo matang", 3),
        # Casual - Male - Light Skin
        ("Pakaian santai untuk pria berkulit cerah", 4),
        ("Baju casual cowok kulit putih", 4),
        ("Outfit santai untuk laki-laki dengan kulit terang", 4),
        ("Rekomendasi baju hangout untuk pria berkulit cerah", 4),
        ("Pakaian jalan-jalan untuk cowok kulit putih", 4),
        # Casual - Female - Light Skin
        ("Baju santai untuk wanita berkulit cerah", 5),
        ("Outfit casual untuk cewek kulit putih", 5),
        ("Pakaian jalan-jalan untuk perempuan berkulit terang", 5),
        ("Rekomendasi baju hangout untuk wanita kulit cerah", 5),
        ("Baju santai apa yang cocok untuk cewek berkulit terang?", 5),
        # Casual - Male - Dark Skin
        ("Pakaian santai untuk pria berkulit sawo matang", 6),
        ("Baju casual untuk cowok kulit gelap", 6),
        ("Outfit hangout untuk laki-laki dengan kulit coklat", 6),
        ("Rekomendasi baju santai pria berkulit gelap", 6),
        ("Pakaian jalan-jalan untuk cowok sawo matang", 6),
        # Casual - Female - Dark Skin
        ("Baju santai untuk wanita berkulit sawo matang", 7),
        ("Outfit casual untuk cewek kulit gelap", 7),
        ("Pakaian jalan-jalan untuk perempuan berkulit coklat", 7),
        ("Rekomendasi baju hangout untuk wanita kulit gelap", 7),
        ("Baju santai apa yang cocok untuk cewek sawo matang?", 7),
        # Wedding
        ("Baju untuk ke pernikahan", 8),
        ("Outfit yang cocok untuk acara wedding", 8),
        ("Pakaian untuk menghadiri resepsi pernikahan", 8),
        ("Rekomendasi baju untuk ke pesta nikah", 8),
        ("Baju apa yang cocok untuk acara akad nikah?", 8),
        # Party
        ("Outfit untuk ke pesta ulang tahun", 9),
        ("Baju pesta malam yang bagus", 9),
        ("Pakaian untuk cocktail party", 9),
        ("Rekomendasi outfit untuk pesta tahun baru", 9),
        ("Baju yang cocok untuk pesta formal", 9),
        # Business Meeting
        ("Pakaian untuk meeting bisnis", 10),
        ("Outfit untuk rapat dengan klien", 10),
        ("Baju yang cocok untuk presentasi bisnis", 10),
        ("Rekomendasi pakaian untuk rapat direksi", 10),
        ("Baju untuk business lunch", 10),
        # Hot Weather
        ("Baju untuk cuaca panas", 11),
        ("Pakaian yang nyaman di hari yang terik", 11),
        ("Outfit untuk musim kemarau", 11),
        ("Rekomendasi baju saat cuaca gerah", 11),
        ("Pakaian yang sejuk untuk cuaca panas", 11),
        # Cold Weather
        ("Baju untuk cuaca dingin", 12),
        ("Pakaian yang hangat untuk musim dingin", 12),
        ("Outfit untuk ke pegunungan", 12),
        ("Rekomendasi pakaian saat cuaca sejuk", 12),
        ("Baju tebal untuk cuaca dingin", 12),
        # Rainy Weather
        ("Baju untuk musim hujan", 13),
        ("Pakaian yang cocok saat hujan", 13),
        ("Outfit anti air untuk cuaca hujan", 13),
        ("Rekomendasi baju untuk hari yang gerimis", 13),
        ("Pakaian yang cocok untuk cuaca hujan", 13),
        # Windy Weather
        ("Baju untuk cuaca berangin", 14),
        ("Pakaian yang cocok saat angin kencang", 14),
        ("Outfit untuk hari yang berangin", 14),
        ("Rekomendasi baju saat cuaca berangin", 14),
        ("Pakaian yang tidak mudah terbawa angin", 14),
        # Summer
        ("Baju untuk musim panas", 15),
        ("Pakaian yang cocok untuk summer", 15),
        ("Outfit musim panas yang nyaman", 15),
        ("Rekomendasi baju untuk liburan musim panas", 15),
        ("Pakaian yang trendy untuk musim panas", 15),
        # Winter
        ("Baju untuk musim dingin", 16),
        ("Pakaian hangat untuk winter", 16),
        ("Outfit musim dingin yang stylish", 16),
        ("Rekomendasi baju untuk liburan winter", 16),
        ("Pakaian yang tebal untuk musim dingin", 16),
        # Spring
        ("Baju untuk musim semi", 17),
        ("Pakaian yang cocok untuk spring", 17),
        ("Outfit musim semi yang stylish", 17),
        ("Rekomendasi baju untuk musim bunga", 17),
        ("Pakaian yang trendy untuk musim semi", 17),
        # Autumn
        ("Baju untuk musim gugur", 18),
        ("Pakaian yang cocok untuk autumn", 18),
        ("Outfit musim gugur yang stylish", 18),
        ("Rekomendasi baju untuk fall season", 18),
        ("Pakaian yang trendy untuk musim gugur", 18),
        # Other
        ("Bantu saya memilih baju", 19),
        ("Apa warna yang sedang trend?", 19),
        ("Bagaimana cara mix and match pakaian?", 19),
        ("Tips fashion untuk pemula", 19),
        ("Brand pakaian yang bagus", 19),
    ]

    # Create DataFrame
    df = pd.DataFrame(test_cases, columns=["query", "expected_intent"])

    return df


def test_nlp_processor(model_path="./fine-tuned-model"):
    """Test the NLP processor with various fashion queries."""
    try:
        # Create results directory
        results_dir = "test_results"
        os.makedirs(results_dir, exist_ok=True)

        # Get test data
        test_data = create_test_data()
        print(f"Created {len(test_data)} test cases")

        # Initialize the model
        print("Initializing IndoBERT model...")
        start_time = time.time()
        processor = IndoBERTFashionProcessor(model_path)
        model_load_time = time.time() - start_time
        print(f"Model loaded in {model_load_time:.2f} seconds")

        # Test each query
        results = []
        for i, row in test_data.iterrows():
            query = row["query"]
            expected_intent = row["expected_intent"]

            # Time the classification
            start_time = time.time()
            predicted_intent = processor.classify_intent(query)
            processing_time = time.time() - start_time

            # Store result
            result = {
                "query": query,
                "expected_intent": expected_intent,
                "predicted_intent": predicted_intent,
                "processing_time": processing_time,
                "is_correct": expected_intent == predicted_intent,
            }
            results.append(result)

            # Print progress
            if (i + 1) % 10 == 0:
                print(f"Processed {i+1}/{len(test_data)} queries...")

        # Create results DataFrame
        results_df = pd.DataFrame(results)

        # Calculate accuracy
        accuracy = results_df["is_correct"].mean()
        avg_processing_time = results_df["processing_time"].mean()

        # Generate classification report
        y_true = results_df["expected_intent"]
        y_pred = results_df["predicted_intent"]
        class_report = classification_report(y_true, y_pred, output_dict=True)

        # Create confusion matrix
        cm = confusion_matrix(y_true, y_pred)

        # Plot confusion matrix
        plt.figure(figsize=(12, 10))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
        plt.xlabel("Predicted Intent")
        plt.ylabel("True Intent")
        plt.title("Confusion Matrix")
        plt.tight_layout()

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save confusion matrix plot
        cm_file = os.path.join(results_dir, f"nlp_confusion_matrix_{timestamp}.png")
        plt.savefig(cm_file)
        plt.close()

        # Save detailed results
        results_file = os.path.join(results_dir, f"nlp_test_results_{timestamp}.csv")
        results_df.to_csv(results_file, index=False)

        # Create summary
        summary = {
            "timestamp": timestamp,
            "total_queries": len(results),
            "accuracy": accuracy,
            "average_processing_time": avg_processing_time,
            "classification_report": class_report,
        }

        # Save summary
        summary_file = os.path.join(results_dir, f"nlp_test_summary_{timestamp}.json")
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        # Print summary
        print("\n" + "=" * 60)
        print(f"NLP Test Summary:")
        print("-" * 60)
        print(f"Total Queries: {len(results)}")
        print(f"Accuracy: {accuracy:.2%}")
        print(f"Average Processing Time: {avg_processing_time:.4f} seconds")
        print("-" * 60)
        print("Classification Report:")
        print(classification_report(y_true, y_pred))
        print("=" * 60)
        print(f"Detailed results saved to: {results_file}")
        print(f"Summary saved to: {summary_file}")
        print(f"Confusion matrix saved to: {cm_file}")

        return summary, results_df

    except Exception as e:
        print(f"Error in NLP testing: {str(e)}")
        import traceback

        traceback.print_exc()
        return None, None


if __name__ == "__main__":
    test_nlp_processor()
