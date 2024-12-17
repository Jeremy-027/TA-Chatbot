# src/combine_datasets.py
import pandas as pd
from dataset_generator import FashionDatasetGenerator
import os

# Create directories if they don't exist
os.makedirs("data/processed", exist_ok=True)

# Load your original dataset
original_df = pd.read_csv("train/dataset.csv")
print(f"Original dataset size: {len(original_df)}")

# Generate new data
generator = FashionDatasetGenerator()
generated_df = generator.generate_dataset()
print(f"Generated dataset size: {len(generated_df)}")

# Combine datasets
combined_df = pd.concat([original_df, generated_df], ignore_index=True)

# Remove any duplicates
combined_df = combined_df.drop_duplicates(subset=["query"])
print(f"Combined dataset size after removing duplicates: {len(combined_df)}")

# Save the combined dataset
combined_df.to_csv("data/processed/combined_dataset.csv", index=False)
print("Combined dataset saved to data/processed/combined_dataset.csv")

# Display a few examples
print("\nSample from combined dataset:")
print(combined_df.sample(5)[["query", "response", "label"]])
