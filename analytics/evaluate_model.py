# analytics/evaluate_model.py
import matplotlib.pyplot as plt
import pandas as pd
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
)
import seaborn as sns
import numpy as np


def load_data():
    """Load train and test datasets"""
    train_df = pd.read_csv("train/train_dataset.csv")
    test_df = pd.read_csv("train/test_dataset.csv")
    return train_df, test_df


def evaluate_model(model_path, test_df):
    """Evaluate model on test data"""
    # Load model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Setup outputs
    y_true = []
    y_pred = []
    confidences = []

    # Generate predictions
    model.eval()
    with torch.no_grad():
        for idx, row in test_df.iterrows():
            # Tokenize
            inputs = tokenizer(
                row["query"],
                return_tensors="pt",
                padding="max_length",
                truncation=True,
                max_length=128,
            ).to(device)

            # Predict
            outputs = model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)
            pred_class = torch.argmax(probs, dim=1).item()
            confidence = probs[0][pred_class].item()

            # Store
            y_true.append(row["label"])
            y_pred.append(pred_class)
            confidences.append(confidence)

            # Show progress
            if (idx + 1) % 50 == 0:
                print(f"Evaluated {idx+1}/{len(test_df)} examples")

    # Calculate metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average="weighted"
    )

    metrics = {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1}

    print("\nEvaluation Results:")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")

    return y_true, y_pred, confidences, metrics


def visualize_results(train_df, test_df, y_true, y_pred, confidences, metrics):
    """Generate visualizations for model evaluation"""
    # Create output directory
    os.makedirs("analytics/graphs", exist_ok=True)

    # 1. Plot label distribution
    plt.figure(figsize=(12, 6))
    train_counts = train_df["label"].value_counts().sort_index()
    test_counts = test_df["label"].value_counts().sort_index()

    df_counts = pd.DataFrame({"Train": train_counts, "Test": test_counts}).fillna(0)

    df_counts.plot(kind="bar")
    plt.title("Label Distribution in Train and Test Sets")
    plt.xlabel("Label")
    plt.ylabel("Count")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("analytics/graphs/label_distribution.png")
    plt.close()

    # 2. Plot confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(14, 12))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig("analytics/graphs/confusion_matrix.png")
    plt.close()

    # 3. Confidence distribution
    plt.figure(figsize=(10, 6))
    plt.hist(confidences, bins=20, alpha=0.7)
    plt.axvline(x=0.5, color="r", linestyle="--")
    plt.title("Prediction Confidence Distribution")
    plt.xlabel("Confidence")
    plt.ylabel("Count")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("analytics/graphs/confidence_distribution.png")
    plt.close()

    # 4. Metrics summary
    plt.figure(figsize=(8, 6))
    metrics_series = pd.Series(metrics)
    metrics_series.plot(kind="bar", color="skyblue")
    plt.title("Model Performance Metrics")
    plt.ylabel("Score")
    plt.ylim(0, 1)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    for i, v in enumerate(metrics_series):
        plt.text(i, v + 0.01, f"{v:.4f}", ha="center")
    plt.tight_layout()
    plt.savefig("analytics/graphs/performance_metrics.png")
    plt.close()

    print("Visualizations saved to analytics/graphs/ directory")


if __name__ == "__main__":
    print("Starting model evaluation...")

    # Load data
    train_df, test_df = load_data()
    print(f"Loaded {len(train_df)} training examples and {len(test_df)} test examples")

    # Evaluate model
    y_true, y_pred, confidences, metrics = evaluate_model("./fine-tuned-model", test_df)

    # Visualize results
    visualize_results(train_df, test_df, y_true, y_pred, confidences, metrics)
