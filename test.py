import pandas as pd

metadata = pd.read_csv("test_data/audio_metadata.csv")
print(f"Number of entries in metadata: {len(metadata)}")
