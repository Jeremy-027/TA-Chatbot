# train/train_model.py
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
)
from preprocess import preprocess_dataset
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import numpy as np
import logging
import os


def setup_logging():
    os.makedirs("./results", exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("./results/trainer_log.txt"),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(__name__)


def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average="weighted"
    )
    acc = accuracy_score(labels, preds)
    return {"accuracy": acc, "f1": f1, "precision": precision, "recall": recall}


def train_model():
    # Check if CUDA is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    logger = setup_logging()
    logger.info("Starting training process...")

    # Load preprocessed dataset
    tokenized_datasets = preprocess_dataset()

    # Load model with the correct number of labels
    model = AutoModelForSequenceClassification.from_pretrained(
        "indobert-base-p2", num_labels=20, ignore_mismatched_sizes=True
    )

    # Move model to GPU if available
    model.to(device)

    # Define training arguments with GPU settings
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="steps",
        eval_steps=20,
        learning_rate=1e-5,
        # Increase batch sizes since RTX 3070 has 8GB VRAM
        per_device_train_batch_size=8,  # Increased from 4
        per_device_eval_batch_size=8,  # Increased from 4
        num_train_epochs=15,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        greater_is_better=True,
        save_total_limit=2,
        logging_steps=10,
        warmup_steps=100,
        fp16=True,  # Mixed precision training
        gradient_accumulation_steps=4,  # Added for better memory usage
        dataloader_num_workers=4,  # Utilize more CPU cores for data loading
        # Added for better GPU utilization
        max_grad_norm=1.0,
        gradient_checkpointing=True,  # Trade computation for memory
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"],
        compute_metrics=compute_metrics,
    )

    # Train the model
    print("Starting training...")
    trainer.train()

    # Evaluate the model
    print("\nEvaluating model...")
    eval_results = trainer.evaluate()
    print(f"\nEvaluation Results: {eval_results}")

    # Save the model and tokenizer
    print("\nSaving model...")
    model.save_pretrained("./fine-tuned-model")
    tokenizer = AutoTokenizer.from_pretrained("indobert-base-p2")
    tokenizer.save_pretrained("./fine-tuned-model")
    print("Model and tokenizer saved successfully!")

    logger.info(f"Training arguments: {training_args}")

    # After training, log results
    logger.info(f"Training complete. Evaluation results: {eval_results}")


if __name__ == "__main__":
    train_model()
