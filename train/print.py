from datasets import load_dataset
from transformers import AutoTokenizer

def preprocess_dataset():
    # Load your dataset
    dataset = load_dataset('csv', data_files={'train': 'train/train_dataset.csv', 'test': 'train/test_dataset.csv'})

    # Print the dataset structure
    print(dataset)

    # Initialize tokenizer
    tokenizer = AutoTokenizer.from_pretrained("indobert-base-p2")

    # Preprocess the dataset
    def preprocess_function(examples):
        return tokenizer(examples['query'], truncation=True, padding='max_length', max_length=128)

    tokenized_datasets = dataset.map(preprocess_function, batched=True)
    return tokenized_datasets

if __name__ == "__main__":
    tokenized_datasets = preprocess_dataset()
    print("Dataset preprocessed successfully!")
