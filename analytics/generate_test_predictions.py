# analytics/generate_test_predictions.py
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import pandas as pd
import numpy as np
import os


def generate_test_predictions(model_path, test_file, output_file):
    """Generate predictions for test dataset and save results"""
    print(f"Generating predictions using model from {model_path}")

    # Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)

    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Load test data
    test_df = pd.read_csv(test_file)

    # Initialize lists for results
    true_labels = []
    predicted_labels = []
    confidence_scores = []

    # Generate predictions
    model.eval()
    with torch.no_grad():
        for idx, row in test_df.iterrows():
            # Prepare input
            inputs = tokenizer(
                row["query"],
                return_tensors="pt",
                padding="max_length",
                truncation=True,
                max_length=128,
            ).to(device)

            # Get prediction
            outputs = model(**inputs)
            predictions = torch.softmax(outputs.logits, dim=1)
            predicted_label = torch.argmax(predictions, dim=1).item()
            confidence = predictions[0][predicted_label].item()

            # Store results
            true_labels.append(row["label"])
            predicted_labels.append(predicted_label)
            confidence_scores.append(confidence)

            # Print progress
            if (idx + 1) % 100 == 0:
                print(f"Processed {idx + 1}/{len(test_df)} examples")

    # Create results dataframe
    results_df = pd.DataFrame(
        {
            "query": test_df["query"],
            "true_label": true_labels,
            "predicted_label": predicted_labels,
            "confidence": confidence_scores,
        }
    )

    # Calculate accuracy
    accuracy = (results_df["true_label"] == results_df["predicted_label"]).mean()
    print(f"Test accuracy: {accuracy:.4f}")

    # Save results
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    results_df.to_csv(output_file, index=False)
    print(f"Predictions saved to {output_file}")

    return results_df


if __name__ == "__main__":
    # Paths
    model_path = "./fine-tuned-model"
    test_file = "data/processed/test_dataset.csv"
    output_file = "results/test_predictions.csv"

    # Generate predictions
    predictions_df = generate_test_predictions(model_path, test_file, output_file)
