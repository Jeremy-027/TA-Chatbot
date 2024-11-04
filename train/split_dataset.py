# train/split_dataset.py

import pandas as pd
from sklearn.model_selection import train_test_split

# Load the dataset
df = pd.read_csv('train/dataset.csv')

# Split the dataset
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Save the split datasets, including the label column
train_df.to_csv('train/train_dataset.csv', index=False)
test_df.to_csv('train/test_dataset.csv', index=False)
