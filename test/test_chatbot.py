# test/test_chatbot.py
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.language_model import IndoBERTFashionProcessor


def test_chatbot():
    print("Fashion Chatbot Test Mode")
    print("=" * 50)
    print("Ketik 'keluar' untuk mengakhiri")
    print("=" * 50)

    # Get the correct path to the model
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    model_path = os.path.join(parent_dir, "fine-tuned-model")

    # Check if model exists
    if not os.path.exists(model_path):
        print("Error: Model not found at", model_path)
        print("Please ensure you have trained the model first.")
        return

    processor = IndoBERTFashionProcessor(model_path)

    while True:
        # Get text input
        user_input = input("\nAnda: ")

        if user_input.lower() in ["keluar", "exit", "quit"]:
            print("\nTerima kasih telah menggunakan Fashion Chatbot!")
            break

        try:
            # Process the input
            intent = processor.classify_intent(user_input)
            sentiment = processor.analyze_sentiment(user_input)
            response = processor.generate_response(user_input, intent, sentiment)

            print(f"Asisten: {response}")
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Please try again with a different query.")


if __name__ == "__main__":
    test_chatbot()
