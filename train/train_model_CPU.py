# train/train_model.py
import torch
import pandas as pd
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
)
from preprocess import preprocess_dataset
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import numpy as np
from torch.nn import CrossEntropyLoss


def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average="weighted"
    )
    acc = accuracy_score(labels, preds)
    return {"accuracy": acc, "f1": f1, "precision": precision, "recall": recall}


class CustomTrainer(Trainer):
    def __init__(self, *args, class_weights=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_weights = class_weights

    def compute_loss(
        self, model, inputs, return_outputs=False, num_items_in_batch=None
    ):
        labels = inputs.pop("labels")
        outputs = model(**inputs)
        logits = outputs.logits

        if self.class_weights is not None:
            loss_fct = CrossEntropyLoss(weight=self.class_weights.to(logits.device))
        else:
            loss_fct = CrossEntropyLoss()

        loss = loss_fct(logits.view(-1, self.model.config.num_labels), labels.view(-1))

        return (loss, outputs) if return_outputs else loss


def train_model():
    tokenized_datasets = preprocess_dataset()
    train_df = pd.read_csv("train/train_dataset.csv")
    class_weights = torch.ones(20)

    class_counts = train_df["label"].value_counts()
    total_samples = len(train_df)

    for label in range(20):
        if label in class_counts.index:
            class_weights[label] = total_samples / (20 * class_counts[label])
        else:
            class_weights[label] = 1.0

    model = AutoModelForSequenceClassification.from_pretrained(
        "indobert-base-p2", num_labels=20, ignore_mismatched_sizes=True
    )

    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="steps",
        eval_steps=20,
        learning_rate=1e-5,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        num_train_epochs=15,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        greater_is_better=True,
        save_total_limit=2,
        logging_steps=10,
        warmup_steps=100,
        fp16=True,
    )

    trainer = CustomTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["test"],
        compute_metrics=compute_metrics,
        class_weights=class_weights,
    )

    print("Starting training...")
    trainer.train()

    print("\nEvaluating model...")
    eval_results = trainer.evaluate()
    print(f"\nEvaluation Results: {eval_results}")

    print("\nSaving model...")
    model.save_pretrained("./fine-tuned-model")
    tokenizer = AutoTokenizer.from_pretrained("indobert-base-p2")
    tokenizer.save_pretrained("./fine-tuned-model")
    print("Model and tokenizer saved successfully!")


if __name__ == "__main__":
    train_model()
