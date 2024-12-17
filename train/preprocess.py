# train/preprocess.py
from datasets import load_dataset
from transformers import AutoTokenizer


def preprocess_dataset():
    # Load your dataset
    dataset = load_dataset(
        "csv",
        data_files={
            "train": "train/train_dataset.csv",
            "test": "train/test_dataset.csv",
        },
    )

    # Initialize tokenizer
    tokenizer = AutoTokenizer.from_pretrained("indobert-base-p2")

    # Preprocess function
    def preprocess_function(examples):
        return tokenizer(
            examples["query"], truncation=True, padding="max_length", max_length=128
        )

    # Apply preprocessing
    tokenized_datasets = dataset.map(
        preprocess_function,
        batched=True,
        remove_columns=["query", "response"],  # Remove only query and response columns
    )

    # Make sure all features have the same length
    tokenized_datasets = tokenized_datasets.remove_columns(
        [
            col
            for col in tokenized_datasets["train"].column_names
            if col not in ["input_ids", "attention_mask", "label"]
        ]
    )

    return tokenized_datasets


if __name__ == "__main__":
    try:
        tokenized_datasets = preprocess_dataset()
        print("Dataset preprocessed successfully!")
        print(f"Training set size: {len(tokenized_datasets['train'])}")
        print(f"Test set size: {len(tokenized_datasets['test'])}")
    except Exception as e:
        print(f"Error during preprocessing: {str(e)}")
