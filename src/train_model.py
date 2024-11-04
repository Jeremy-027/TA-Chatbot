# src/train_model.py
import torch  # Add this import
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from preprocess import preprocess_dataset

def train_model():
    # Load preprocessed dataset
    tokenized_datasets = preprocess_dataset()

    # Ensure labels are included in the dataset
    def add_labels(examples):
        examples['labels'] = examples['label']
        return examples

    tokenized_datasets = tokenized_datasets.map(add_labels, batched=True)

    # Verify unique labels
    unique_labels = set(tokenized_datasets['train']['labels'])
    print(f"Unique labels in the training dataset: {unique_labels}")

    # Load IndoBERT model with the correct number of labels
    model = AutoModelForSequenceClassification.from_pretrained(
        "indobert-base-p2",
        num_labels=20,
        ignore_mismatched_sizes=True
    )

    # Reinitialize the classifier layer
    model.classifier = torch.nn.Linear(model.config.hidden_size, 20)
    model.num_labels = 20

    # Define training arguments
    training_args = TrainingArguments(
        output_dir='./results',
        eval_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
    )

    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets['train'],
        eval_dataset=tokenized_datasets['test'],
    )

    # Train the model
    trainer.train()

    # Save the model and tokenizer
    model.save_pretrained('./fine-tuned-model')
    tokenizer = AutoTokenizer.from_pretrained("indobert-base-p2")
    tokenizer.save_pretrained('./fine-tuned-model')
    print("Model and tokenizer trained and saved successfully!")

if __name__ == "__main__":
    train_model()
