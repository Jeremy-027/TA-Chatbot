# analytics/training_visualizer.py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import os
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns


class TrainingVisualizer:
    def __init__(self, results_dir="./results", output_dir="./analytics/graphs"):
        self.results_dir = results_dir
        self.output_dir = output_dir

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Initialize metrics storage
        self.metrics = {
            "loss": {"train": [], "eval": []},
            "accuracy": [],
            "precision": [],
            "recall": [],
            "f1": [],
            "steps": [],
        }

        # Initialize step and epoch tracking
        self.current_step = 0
        self.current_epoch = 0

    def parse_log_file(self, log_file):
        """Extract metrics from training log file"""
        print(f"Parsing log file: {log_file}")

        with open(log_file, "r") as f:
            for line in f:
                try:
                    if "{'loss':" in line or "{'eval_loss':" in line:
                        # Extract the JSON part from the log line
                        json_str = line[line.find("{") : line.rfind("}") + 1]
                        data = json.loads(json_str)

                        # Process training metrics
                        if "loss" in data:
                            self.metrics["loss"]["train"].append(data["loss"])
                            if "step" in data:
                                self.current_step = data["step"]
                                self.metrics["steps"].append(self.current_step)
                            if "epoch" in data:
                                self.current_epoch = data["epoch"]

                        # Process evaluation metrics
                        if "eval_loss" in data:
                            self.metrics["loss"]["eval"].append(data["eval_loss"])
                            if "eval_accuracy" in data:
                                self.metrics["accuracy"].append(data["eval_accuracy"])
                            if "eval_precision" in data:
                                self.metrics["precision"].append(data["eval_precision"])
                            if "eval_recall" in data:
                                self.metrics["recall"].append(data["eval_recall"])
                            if "eval_f1" in data:
                                self.metrics["f1"].append(data["eval_f1"])
                except Exception as e:
                    print(f"Error parsing line: {e}")
                    continue

        print(f"Extracted metrics for {len(self.metrics['steps'])} training steps")

    def plot_training_curves(self):
        """Plot training and evaluation loss curves"""
        plt.figure(figsize=(12, 6))

        # Plot training loss if available
        if len(self.metrics["loss"]["train"]) > 0:
            plt.plot(
                self.metrics["steps"][: len(self.metrics["loss"]["train"])],
                self.metrics["loss"]["train"],
                label="Training Loss",
                color="blue",
            )

        # Plot evaluation loss if available
        if len(self.metrics["loss"]["eval"]) > 0:
            # Use evenly spaced x values since eval is less frequent
            eval_steps = np.linspace(
                0, self.current_step, len(self.metrics["loss"]["eval"])
            )
            plt.plot(
                eval_steps,
                self.metrics["loss"]["eval"],
                label="Evaluation Loss",
                color="red",
                linestyle="--",
            )

        plt.xlabel("Training Steps")
        plt.ylabel("Loss")
        plt.title("Training and Evaluation Loss")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/loss_curves.png")
        plt.close()

        print(f"Loss curves saved to {self.output_dir}/loss_curves.png")

    def plot_performance_metrics(self):
        """Plot accuracy, precision, recall and F1 score"""
        plt.figure(figsize=(12, 6))

        # Create evenly spaced x values for evaluation steps
        eval_steps = np.linspace(0, self.current_step, len(self.metrics["accuracy"]))

        # Plot each metric
        if len(self.metrics["accuracy"]) > 0:
            plt.plot(eval_steps, self.metrics["accuracy"], label="Accuracy", marker="o")
        if len(self.metrics["precision"]) > 0:
            plt.plot(
                eval_steps, self.metrics["precision"], label="Precision", marker="s"
            )
        if len(self.metrics["recall"]) > 0:
            plt.plot(eval_steps, self.metrics["recall"], label="Recall", marker="^")
        if len(self.metrics["f1"]) > 0:
            plt.plot(eval_steps, self.metrics["f1"], label="F1 Score", marker="d")

        plt.xlabel("Training Steps")
        plt.ylabel("Score")
        plt.title("Model Performance Metrics")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/performance_metrics.png")
        plt.close()

        print(f"Performance metrics saved to {self.output_dir}/performance_metrics.png")

    def plot_confusion_matrix(self, y_true, y_pred, labels=None):
        """Plot confusion matrix from test predictions"""
        cm = confusion_matrix(y_true, y_pred)

        plt.figure(figsize=(14, 12))
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="Blues",
            xticklabels=labels,
            yticklabels=labels,
        )
        plt.xlabel("Predicted")
        plt.ylabel("True")
        plt.title("Confusion Matrix")
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/confusion_matrix.png")
        plt.close()

        print(f"Confusion matrix saved to {self.output_dir}/confusion_matrix.png")

    def generate_classification_report(self, y_true, y_pred, labels=None):
        """Generate and save classification report"""
        report = classification_report(
            y_true, y_pred, target_names=labels, output_dict=True
        )
        report_df = pd.DataFrame(report).transpose()

        # Save to CSV
        report_df.to_csv(f"{self.output_dir}/classification_report.csv")

        # Plot as heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(report_df.iloc[:-3, :3], annot=True, cmap="YlGnBu")
        plt.title("Classification Report")
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/classification_report.png")
        plt.close()

        print(
            f"Classification report saved to {self.output_dir}/classification_report.csv"
        )
        print(
            f"Classification report visualization saved to {self.output_dir}/classification_report.png"
        )

    def visualize_label_distribution(self, train_file, test_file):
        """Visualize the distribution of labels in train and test sets"""
        # Load data
        train_df = pd.read_csv(train_file)
        test_df = pd.read_csv(test_file)

        # Count labels
        train_counts = train_df["label"].value_counts().sort_index()
        test_counts = test_df["label"].value_counts().sort_index()

        # Create a dataframe for both
        counts_df = pd.DataFrame({"Train": train_counts, "Test": test_counts}).fillna(0)

        # Plot
        plt.figure(figsize=(14, 8))
        counts_df.plot(kind="bar", ax=plt.gca())
        plt.title("Label Distribution in Train and Test Sets")
        plt.xlabel("Label")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/label_distribution.png")
        plt.close()

        print(
            f"Label distribution visualization saved to {self.output_dir}/label_distribution.png"
        )

    def run_test_evaluation(self, test_predictions_file):
        """Evaluate test predictions and generate visualizations"""
        # Load predictions
        predictions_df = pd.read_csv(test_predictions_file)

        y_true = predictions_df["true_label"].values
        y_pred = predictions_df["predicted_label"].values

        # Get unique labels
        labels = sorted(set(np.concatenate([y_true, y_pred])))

        # Generate label names if available (otherwise use numbers)
        label_names = [f"Label {l}" for l in labels]

        # Generate confusion matrix
        self.plot_confusion_matrix(y_true, y_pred, label_names)

        # Generate classification report
        self.generate_classification_report(y_true, y_pred, label_names)


# Usage example
if __name__ == "__main__":
    visualizer = TrainingVisualizer()

    # Parse training logs (assuming they're in results/trainer_log.txt)
    visualizer.parse_log_file("./results/trainer_log.txt")

    # Generate training curves
    visualizer.plot_training_curves()

    # Generate performance metrics visualization
    visualizer.plot_performance_metrics()

    # Visualize label distribution
    visualizer.visualize_label_distribution(
        "data/processed/train_dataset.csv", "data/processed/test_dataset.csv"
    )

    # If you have test predictions:
    # visualizer.run_test_evaluation("./results/test_predictions.csv")
