# src/chatbot_azure.py
import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
from language_model import IndoBERTFashionProcessor
import logging


class AzureFashionChatbot:
    def __init__(self):
        try:
            load_dotenv()

            if not os.getenv("AZURE_SPEECH_KEY") or not os.getenv(
                "AZURE_SPEECH_REGION"
            ):
                print("Error: Missing required Azure credentials in .env file")
                return

            self.speech_key = os.getenv("AZURE_SPEECH_KEY")
            self.speech_region = os.getenv("AZURE_SPEECH_REGION")

            self.speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key, region=self.speech_region
            )

            self.speech_config.speech_recognition_language = "id-ID"
            self.speech_config.speech_synthesis_language = "id-ID"
            self.speech_config.speech_synthesis_voice_name = "id-ID-GadisNeural"

            self.speech_recognizer = speechsdk.SpeechRecognizer(
                speech_config=self.speech_config
            )
            self.speech_synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config
            )

            self.nlp_processor = IndoBERTFashionProcessor(
                model_path="./fine-tuned-model"
            )
        except Exception as e:
            print(f"Initialization error: {str(e)}")
            raise

    def speech_to_text(self):
        try:
            print("Mendengarkan... (Mulai berbicara)")
            result = self.speech_recognizer.recognize_once()
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                text = result.text
                print(f"Anda mengatakan: {text}")
                return text.lower()
            elif result.reason == speechsdk.ResultReason.NoMatch:
                print("Tidak dapat mengenali suara")
                return ""
            elif result.reason == speechsdk.ResultReason.Canceled:
                print("Speech recognition dibatalkan")
                return ""
        except Exception as e:
            print(f"Error in speech_to_text: {str(e)}")
            return ""

    def text_to_speech(self, text, is_error=False):
        """Convert text to speech using Azure Speech Service"""
        # Don't convert error messages to speech
        if is_error:
            print(text)
            return

        try:
            ssml = f"""
            <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="id-ID">
                <voice name="id-ID-GadisNeural">
                    {text}
                </voice>
            </speak>
            """

            result = self.speech_synthesizer.speak_ssml_async(ssml).get()
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print("Asisten: " + text)
            else:
                error_msg = f"Error dalam sintesis suara: {result.reason}"
                print(error_msg)
                if result.reason == speechsdk.ResultReason.Canceled:
                    cancellation_details = result.cancellation_details
                    print(f"CancellationReason: {cancellation_details.reason}")
                    if (
                        cancellation_details.reason
                        == speechsdk.CancellationReason.Error
                    ):
                        print(f"ErrorDetails: {cancellation_details.error_details}")
        except Exception as e:
            print(f"Error dalam text_to_speech: {str(e)}")

    def process_input(self, text):
        if not text:
            return (
                "Maaf, bisakah Anda mengulangi?",
                True,
            )  # Second parameter indicates if it's an error

        if any(
            word in text.lower()
            for word in ["keluar", "selesai", "quit", "exit", "stop"]
        ):
            return "KELUAR", False

        try:
            intent = self.nlp_processor.classify_intent(text)
            sentiment = self.nlp_processor.analyze_sentiment(text)
            response = self.nlp_processor.generate_response(text, intent, sentiment)
            return response, False
        except Exception as e:
            error_msg = "Maaf, terjadi kesalahan dalam memproses permintaan Anda."
            print(f"Error in process_input: {str(e)}")
            return error_msg, True

    def run(self):
        try:
            welcome_message = (
                "Halo! Saya asisten fashion Anda. Apa jenis pakaian yang Anda cari?"
            )
            print("\n" + "=" * 50)
            print("Fashion Chatbot Indonesia")
            print("Katakan 'keluar' untuk mengakhiri percakapan")
            print("=" * 50 + "\n")

            self.text_to_speech(welcome_message)

            while True:
                user_input = self.speech_to_text()
                if not user_input:
                    continue

                response, is_error = self.process_input(user_input)
                if response == "KELUAR":
                    farewell = (
                        "Terima kasih telah menggunakan Fashion Chatbot. Sampai jumpa!"
                    )
                    self.text_to_speech(farewell)
                    break

                self.text_to_speech(response, is_error)

        except Exception as e:
            print(f"Error in main loop: {str(e)}")


if __name__ == "__main__":
    try:
        chatbot = AzureFashionChatbot()
        chatbot.run()
    except Exception as e:
        print(f"Critical error: {str(e)}")
