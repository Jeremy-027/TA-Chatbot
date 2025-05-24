# Create a simple script to set up the directory
import os


def create_real_world_test_directory():
    """Create directory for real-world test files."""
    real_world_dir = "test_data/audio_samples/real_world"
    os.makedirs(real_world_dir, exist_ok=True)
    print(f"Created directory: {real_world_dir}")
    print("Please record your real-world test files and save them in this directory.")

    # Print suggested scenarios to record
    scenarios = [
        "Saya mencari baju formal untuk interview kerja",
        "Rekomendasi pakaian casual untuk jalan-jalan",
        "Baju apa yang cocok untuk cuaca panas",
        "Outfit untuk ke pesta pernikahan teman",
        "Warna apa yang bagus untuk kulit sawo matang",
        "Saya pria mau ke interview kerja, sebaiknya pakai apa",
        "Pakaian santai untuk wanita berkulit cerah",
        "Baju yang cocok untuk musim hujan",
        "Aksesoris apa yang cocok dengan kemeja putih",
        "Rekomendasi pakaian untuk ke kantor",
        "Fashion yang sedang trend untuk pria",
        "Cara mix and match kemeja biru",
    ]

    print("\nSuggested phrases to record:")
    for i, text in enumerate(scenarios, 1):
        print(f'{i}. "{text}"')

    print(
        "\nSave files with names like: rw_formal_query.wav, rw_casual_query.wav, etc."
    )


if __name__ == "__main__":
    create_real_world_test_directory()
