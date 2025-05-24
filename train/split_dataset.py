# train/split_dataset.py
import pandas as pd
from sklearn.model_selection import train_test_split
import os

# Load the combined dataset
df = pd.read_csv("data/processed/combined_enhanced_dataset.csv")
print(f"Total dataset size: {len(df)}")

# Print label distribution
print("\nLabel distribution:")
label_counts = df["label"].value_counts()
for label, count in label_counts.items():
    print(f"Label {label}: {count} examples")

# Split without stratification since we have too few examples in some classes
train_df, test_df = train_test_split(
    df, test_size=0.2, random_state=42, stratify=df["label"]
)

print(f"\nTraining set size: {len(train_df)}")
print(f"Testing set size: {len(test_df)}")

# Print distribution in splits
print("\nTraining set distribution:")
train_labels = train_df["label"].value_counts()
for label, count in train_labels.items():
    print(f"Label {label}: {count} examples")

print("\nTest set distribution:")
test_labels = test_df["label"].value_counts()
for label, count in test_labels.items():
    print(f"Label {label}: {count} examples")

# Save the split datasets
train_df.to_csv("train/train_dataset.csv", index=False)
test_df.to_csv("train/test_dataset.csv", index=False)
print("\nDatasets saved successfully!")
