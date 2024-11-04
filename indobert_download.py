import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def download_indobert():
    """Download and cache the IndoBERT model"""
    # Check if model is already downloaded
    if os.path.exists("indobert-base-p2"):
        print("IndoBERT model already downloaded.")
        return

    # Download the model
    print("Downloading IndoBERT model...")
    tokenizer = AutoTokenizer.from_pretrained("indobenchmark/indobert-base-p2")
    model = AutoModelForSequenceClassification.from_pretrained("indobenchmark/indobert-base-p2")

    # Save the model
    tokenizer.save_pretrained("indobert-base-p2")
    model.save_pretrained("indobert-base-p2")

    print("IndoBERT model download complete.")

if __name__ == "__main__":
    download_indobert()