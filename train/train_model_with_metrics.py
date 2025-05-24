# train/train_model_with_metrics.py
import torch
import matplotlib

matplotlib.use("Agg")  # Use non-interactive backend that doesn't require a display
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
)
from preprocess import preprocess_dataset
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
)
import numpy as np
import logging
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime
import json
from transformers.trainer_callback import TrainerCallback


def setup_logging():
    """Set up logging with timestamped directory."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = f"./results/run_{timestamp}"
    os.makedirs(run_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(f"{run_dir}/trainer_log.txt"),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(__name__), run_dir


class MetricsCallback(TrainerCallback):
    """Callback to track and visualize metrics during training."""

    def __init__(self, run_dir):
        self.run_dir = run_dir
        self.metrics_history = {
            "training_loss": [],
            "eval_loss": [],
            "eval_accuracy": [],
            "eval_f1": [],
            "eval_precision": [],
            "eval_recall": [],
            "learning_rate": [],
            "epoch": [],
            "step": [],
        }
        # Create a debug log file
        self.debug_log_path = f"{run_dir}/metrics_debug.log"
        with open(self.debug_log_path, "w") as f:
            f.write("MetricsCallback initialized\n")

    def on_log(self, args, state, control, logs=None, **kwargs):
        """Called when logs are returned."""
        if logs is not None:
            with open(self.debug_log_path, "a") as f:
                f.write(
                    f"Log received at step {state.global_step}. Available keys: {list(logs.keys())}\n"
                )

            # Track training loss correctly
            if "loss" in logs:
                self.metrics_history["training_loss"].append(logs["loss"])
                with open(self.debug_log_path, "a") as f:
                    f.write(f"Training loss recorded: {logs['loss']}\n")

            # Track other metrics
            for key in logs:
                if key in self.metrics_history:
                    self.metrics_history[key].append(logs[key])

            # Track the current step and epoch
            if state.global_step is not None:
                # Only add step if it's a new step
                if (
                    not self.metrics_history["step"]
                    or state.global_step != self.metrics_history["step"][-1]
                ):
                    self.metrics_history["step"].append(state.global_step)

            if state.epoch is not None:
                self.metrics_history["epoch"].append(state.epoch)

            # Save metrics after each log
            self.save_metrics()

        return control

    def on_evaluate(self, args, state, control, metrics=None, **kwargs):
        """Called after evaluation."""
        if metrics is not None:
            with open(self.debug_log_path, "a") as f:
                f.write(f"Evaluation metrics received: {metrics}\n")

            # Record evaluation metrics
            for key, value in metrics.items():
                if key in self.metrics_history:
                    self.metrics_history[key].append(value)

            # Ensure step is recorded for this evaluation
            if state.global_step is not None and (
                not self.metrics_history["step"]
                or state.global_step != self.metrics_history["step"][-1]
            ):
                self.metrics_history["step"].append(state.global_step)

            self.save_metrics()

        return control

    def save_metrics(self):
        """Save metrics to JSON and generate plots."""
        # Save as JSON
        with open(f"{self.run_dir}/metrics_history.json", "w") as f:
            json.dump(self.metrics_history, f, indent=2)

        # Generate plots
        self.plot_metrics()

    def plot_metrics(self):
        """Generate and save visualization plots for metrics."""
        # Create a directory for plots
        plots_dir = f"{self.run_dir}/plots"
        os.makedirs(plots_dir, exist_ok=True)

        # Plot loss
        self._plot_loss_curves(plots_dir)

        # Plot evaluation metrics
        self._plot_eval_metrics(plots_dir)

        # Plot learning rate
        self._plot_learning_rate(plots_dir)

    def _plot_loss_curves(self, plots_dir):
        """Plot training and validation loss curves."""
        plt.figure(figsize=(10, 6))

        # Plot training loss if available
        if (
            len(self.metrics_history["training_loss"]) > 0
            and len(self.metrics_history["step"]) > 0
        ):
            # Ensure we have enough steps for all training loss points
            train_steps = self.metrics_history["step"][
                : len(self.metrics_history["training_loss"])
            ]
            if len(train_steps) < len(self.metrics_history["training_loss"]):
                train_steps = train_steps + list(
                    range(
                        train_steps[-1] + 1,
                        train_steps[-1]
                        + 1
                        + len(self.metrics_history["training_loss"])
                        - len(train_steps),
                    )
                )

            plt.plot(
                train_steps,
                self.metrics_history["training_loss"],
                label="Training Loss",
                marker="o",
                markersize=3,
            )
            has_training_loss = True
        else:
            has_training_loss = False

        # Plot validation loss if available
        if (
            len(self.metrics_history["eval_loss"]) > 0
            and len(self.metrics_history["step"]) > 0
        ):
            # Get unique evaluation steps
            eval_step_indices = []
            for i, step in enumerate(self.metrics_history["step"]):
                if i > 0 and step == self.metrics_history["step"][i - 1]:
                    continue
                eval_step_indices.append(i)

            # Use unique steps and corresponding eval_loss values
            if len(eval_step_indices) >= len(self.metrics_history["eval_loss"]):
                eval_steps = [
                    self.metrics_history["step"][i]
                    for i in eval_step_indices[: len(self.metrics_history["eval_loss"])]
                ]
            else:
                # Create steps if we don't have enough
                eval_steps = [
                    self.metrics_history["step"][i] for i in eval_step_indices
                ]
                last_step = eval_steps[-1] if eval_steps else 0
                eval_steps.extend(
                    [
                        last_step + (i + 1) * 20
                        for i in range(
                            len(self.metrics_history["eval_loss"]) - len(eval_steps)
                        )
                    ]
                )

            plt.plot(
                eval_steps,
                self.metrics_history["eval_loss"],
                label="Validation Loss",
                marker="x",
                markersize=4,
            )

        plt.xlabel("Training Steps")
        plt.ylabel("Loss")

        # Use appropriate title based on what data is available
        if has_training_loss:
            plt.title("Training and Validation Loss Over Time")
        else:
            plt.title("Validation Loss Over Time")

        plt.legend()
        plt.grid(True)
        plt.savefig(f"{plots_dir}/loss_curve.png")
        plt.close()

    def _plot_eval_metrics(self, plots_dir):
        """Plot evaluation metrics (accuracy, F1, precision, recall)."""
        metrics = ["eval_accuracy", "eval_f1", "eval_precision", "eval_recall"]

        # Check if we have at least one metric with data
        if not any(len(self.metrics_history[m]) > 0 for m in metrics):
            return

        plt.figure(figsize=(10, 6))

        # Plot each metric that has values
        for metric in metrics:
            if len(self.metrics_history[metric]) > 0:
                values = self.metrics_history[metric]

                # Create or align steps for the metrics
                if len(self.metrics_history["step"]) > 0:
                    # Get evaluation steps - use unique steps only
                    eval_step_indices = []
                    for i, step in enumerate(self.metrics_history["step"]):
                        if i > 0 and step == self.metrics_history["step"][i - 1]:
                            continue
                        eval_step_indices.append(i)

                    if len(eval_step_indices) >= len(values):
                        steps = [
                            self.metrics_history["step"][i]
                            for i in eval_step_indices[: len(values)]
                        ]
                    else:
                        # Create steps if we don't have enough
                        steps = [
                            self.metrics_history["step"][i] for i in eval_step_indices
                        ]
                        last_step = steps[-1] if steps else 0
                        steps.extend(
                            [
                                last_step + (i + 1) * 20
                                for i in range(len(values) - len(steps))
                            ]
                        )
                else:
                    # If no steps recorded, create artificial steps
                    steps = list(range(0, len(values) * 20, 20))

                plt.plot(
                    steps,
                    values,
                    label=metric.replace("eval_", "").capitalize(),
                    marker="o",
                    markersize=4,
                )

        # Set proper y-axis limits to show the full range of values
        all_values = []
        for metric in metrics:
            if len(self.metrics_history[metric]) > 0:
                all_values.extend(self.metrics_history[metric])

        if all_values:
            min_val = max(0, min(all_values) - 0.05)
            max_val = min(1.0, max(all_values) + 0.05)
            plt.ylim(min_val, max_val)

        plt.xlabel("Training Steps")
        plt.ylabel("Score")
        plt.title("Evaluation Metrics Over Time")
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{plots_dir}/metrics_curve.png")
        plt.close()

    def _plot_learning_rate(self, plots_dir):
        """Plot learning rate curve."""
        if len(self.metrics_history["learning_rate"]) > 0:
            plt.figure(figsize=(10, 6))

            # Align learning rate and steps
            if len(self.metrics_history["step"]) > 0:
                # Get unique steps
                step_indices = []
                for i, step in enumerate(self.metrics_history["step"]):
                    if i > 0 and step == self.metrics_history["step"][i - 1]:
                        continue
                    step_indices.append(i)

                if len(step_indices) >= len(self.metrics_history["learning_rate"]):
                    steps = [
                        self.metrics_history["step"][i]
                        for i in step_indices[
                            : len(self.metrics_history["learning_rate"])
                        ]
                    ]
                else:
                    # Create steps if we don't have enough
                    steps = [self.metrics_history["step"][i] for i in step_indices]
                    last_step = steps[-1] if steps else 0
                    steps.extend(
                        [
                            last_step + (i + 1) * 20
                            for i in range(
                                len(self.metrics_history["learning_rate"]) - len(steps)
                            )
                        ]
                    )
            else:
                # If no steps recorded, create artificial steps
                steps = list(range(len(self.metrics_history["learning_rate"])))

            plt.plot(
                steps,
                self.metrics_history["learning_rate"],
                label="Learning Rate",
                marker=".",
                markersize=3,
            )

            plt.xlabel("Training Steps")
            plt.ylabel("Learning Rate")
            plt.title("Learning Rate Schedule")
            plt.grid(True)
            plt.savefig(f"{plots_dir}/learning_rate.png")
            plt.close()


def compute_metrics(pred):
    """Compute evaluation metrics from predictions."""
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average="weighted"
    )
    acc = accuracy_score(labels, preds)
    return {"accuracy": acc, "f1": f1, "precision": precision, "recall": recall}


def plot_confusion_matrix(y_true, y_pred, run_dir, num_classes=20):
    """Plot confusion matrix and save it."""
    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(12, 10))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=range(num_classes),
        yticklabels=range(num_classes),
    )
    plt.xlabel("Predicted Labels")
    plt.ylabel("True Labels")
    plt.title("Confusion Matrix")

    plots_dir = f"{run_dir}/plots"
    os.makedirs(plots_dir, exist_ok=True)
    plt.savefig(f"{plots_dir}/confusion_matrix.png")
    plt.close()

    # Normalize confusion matrix
    cm_norm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]

    plt.figure(figsize=(12, 10))
    sns.heatmap(
        cm_norm,
        annot=True,
        fmt=".2f",
        cmap="Blues",
        xticklabels=range(num_classes),
        yticklabels=range(num_classes),
    )
    plt.xlabel("Predicted Labels")
    plt.ylabel("True Labels")
    plt.title("Normalized Confusion Matrix")
    plt.savefig(f"{plots_dir}/confusion_matrix_normalized.png")
    plt.close()


def plot_label_distribution(datasets, run_dir):
    """Plot label distribution in train and test sets."""
    train_labels = datasets["train"]["label"]
    test_labels = datasets["test"]["label"]

    plt.figure(figsize=(12, 6))

    # Plot train distribution
    plt.subplot(1, 2, 1)
    train_counts = pd.Series(train_labels).value_counts().sort_index()
    sns.barplot(x=train_counts.index, y=train_counts.values)
    plt.title("Training Set Label Distribution")
    plt.xlabel("Label")
    plt.ylabel("Count")
    plt.xticks(rotation=90)

    # Plot test distribution
    plt.subplot(1, 2, 2)
    test_counts = pd.Series(test_labels).value_counts().sort_index()
    sns.barplot(x=test_counts.index, y=test_counts.values)
    plt.title("Test Set Label Distribution")
    plt.xlabel("Label")
    plt.ylabel("Count")
    plt.xticks(rotation=90)

    plt.tight_layout()

    plots_dir = f"{run_dir}/plots"
    os.makedirs(plots_dir, exist_ok=True)
    plt.savefig(f"{plots_dir}/label_distribution.png")
    plt.close()


def train_model():
    """Train the model and generate metrics and visualizations."""
    # Check if CUDA is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Setup logging and create run directory
    logger, run_dir = setup_logging()
    logger.info("Starting training process...")
    logger.info(f"Run directory: {run_dir}")

    # Load preprocessed dataset
    tokenized_datasets = preprocess_dataset()

    # Plot dataset statistics
    plot_label_distribution(tokenized_datasets, run_dir)

    # Load model with the correct number of labels
    model = AutoModelForSequenceClassification.from_pretrained(
        "indobert-base-p2", num_labels=20, ignore_mismatched_sizes=True
    )

    # Move model to GPU if available
    model.to(device)

    # Define training arguments with GPU settings
    training_args = TrainingArguments(
        output_dir=run_dir,
        evaluation_strategy="steps",
        eval_steps=20,
        learning_rate=5e-6,  # Lowered from 1e-5 for enhanced dataset
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=10,  # Reduced from 15 for enhanced dataset
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        greater_is_better=True,
        save_total_limit=2,
        logging_steps=10,  # Log every 10 steps
        logging_dir=f"{run_dir}/logs",
        warmup_steps=100,
        fp16=True,
        gradient_accumulation_steps=4,
        dataloader_num_workers=4,
        max_grad_norm=1.0,
        gradient_checkpointing=True,
    )

    # Create metrics callback
    metrics_callback = MetricsCallback(run_dir)

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"],
        compute_metrics=compute_metrics,
        callbacks=[metrics_callback],
    )

    # Train the model
    print("Starting training...")
    trainer.train()

    # Evaluate the model
    print("\nEvaluating model...")
    eval_results = trainer.evaluate()
    print(f"\nEvaluation Results: {eval_results}")

    # Generate confusion matrix
    # Get predictions
    print("\nGenerating predictions for confusion matrix...")
    predictions = trainer.predict(tokenized_datasets["test"])
    y_true = predictions.label_ids
    y_pred = predictions.predictions.argmax(-1)

    # Save prediction arrays for post-training analysis
    np.save(f"{run_dir}/predictions.npy", predictions.predictions)
    np.save(f"{run_dir}/labels.npy", y_true)

    # Plot confusion matrix
    plot_confusion_matrix(y_true, y_pred, run_dir)

    # Save evaluation results
    with open(f"{run_dir}/eval_results.json", "w") as f:
        json.dump(eval_results, f, indent=2)

    # Save the model and tokenizer
    model_dir = f"{run_dir}/model"
    os.makedirs(model_dir, exist_ok=True)
    print(f"\nSaving model to {model_dir}...")
    model.save_pretrained(model_dir)
    tokenizer = AutoTokenizer.from_pretrained("indobert-base-p2")
    tokenizer.save_pretrained(model_dir)
    print("Model and tokenizer saved successfully!")

    # Copy the best model to the fine-tuned-model directory (for backward compatibility)
    os.makedirs("./fine-tuned-model", exist_ok=True)
    model.save_pretrained("./fine-tuned-model")
    tokenizer.save_pretrained("./fine-tuned-model")

    # Log training arguments and final results
    logger.info(f"Training arguments: {training_args}")
    logger.info(f"Training complete. Evaluation results: {eval_results}")

    print(f"\nTraining completed! Metrics and plots saved to {run_dir}/plots")
    return run_dir


def plot_per_class_metrics(y_true, y_pred, run_dir, num_classes=20):
    """Plot per-class precision, recall, and F1 score."""
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average=None, labels=range(num_classes)
    )

    # Create a DataFrame for easy plotting
    metrics_df = pd.DataFrame(
        {
            "Precision": precision,
            "Recall": recall,
            "F1-Score": f1,
            "Class": range(num_classes),
        }
    )

    # Plot metrics
    plt.figure(figsize=(14, 8))
    metrics_df_melted = pd.melt(
        metrics_df,
        id_vars=["Class"],
        value_vars=["Precision", "Recall", "F1-Score"],
        var_name="Metric",
        value_name="Score",
    )

    sns.barplot(x="Class", y="Score", hue="Metric", data=metrics_df_melted)
    plt.title("Per-Class Performance Metrics")
    plt.xlabel("Class Label")
    plt.ylabel("Score")
    plt.ylim(0, 1.0)
    plt.legend(title="Metric")
    plt.grid(axis="y")

    plots_dir = f"{run_dir}/plots"
    os.makedirs(plots_dir, exist_ok=True)
    plt.savefig(f"{plots_dir}/per_class_metrics.png")
    plt.close()

    # Save metrics to CSV for reference
    metrics_df.to_csv(f"{plots_dir}/per_class_metrics.csv", index=False)


if __name__ == "__main__":
    run_dir = train_model()

    # Load predictions for additional analysis
    try:
        print("Performing post-training analysis...")

        with open(f"{run_dir}/eval_results.json", "r") as f:
            eval_results = json.load(f)
            print(f"Final evaluation results: {eval_results}")

        # If you have saved predictions
        predictions_file = f"{run_dir}/predictions.npy"
        labels_file = f"{run_dir}/labels.npy"

        if os.path.exists(predictions_file) and os.path.exists(labels_file):
            predictions = np.load(predictions_file)
            labels = np.load(labels_file)

            # Generate per-class metrics
            print("Generating per-class metrics...")
            plot_per_class_metrics(labels, predictions.argmax(-1), run_dir)
            print("Per-class metrics saved.")
        else:
            print(
                f"Warning: Could not find prediction files for post-training analysis."
            )
    except Exception as e:
        print(f"Error in post-training analysis: {str(e)}")
