import pandas as pd

# Load the dataset
df = pd.read_csv('train/train_dataset.csv')
print(df['label'].unique())
