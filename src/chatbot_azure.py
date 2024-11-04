# src/chatbot_azure.py
import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
from language_model import IndoBERTProcessor
import logging

logging.basicConfig(level=logging.INFO)

class AzureFashionChatbot:
    def __init__(self):
        load_dotenv()

        self.speech_key = os.getenv('AZURE_SPEECH_KEY')
        self.speech_region = os.getenv('AZURE_SPEECH_REGION')

        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key,
            region=self.speech_region
        )

        self.speech_config.speech_recognition_language = "id-ID"
        self.speech_config.speech_synthesis_language = "id-ID"
        self.speech_config.speech_synthesis_voice_name = "id-ID-GadisNeural"

        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config)
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)

        self.nlp_processor = IndoBERTProcessor(model_path='./fine-tuned-model')

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
            logging.error(f"Error in speech_to_text: {str(e)}")
            return ""

    def text_to_speech(self, text):
        """Convert text to speech using Azure Speech Service"""
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
                print(f"Error dalam sintesis suara: {result.reason}")
                if result.reason == speechsdk.ResultReason.Canceled:
                    cancellation_details = result.cancellation_details
                    print(f"CancellationReason: {cancellation_details.reason}")
                    if cancellation_details.reason == speechsdk.CancellationReason.Error:
                        print(f"ErrorDetails: {cancellation_details.error_details}")
                        print("Did you set the speech resource key and region values?")
        except Exception as ex:
            print(f"Error dalam text_to_speech: {str(ex)}")

    def process_input(self, text):
        if not text:
            return "Maaf, bisakah Anda mengulangi?"

        if any(word in text.lower() for word in ["keluar", "selesai", "quit", "exit", "stop"]):
            return "KELUAR"

        try:
            intent = self.nlp_processor.classify_intent(text)
            sentiment = self.nlp_processor.analyze_sentiment(text)
            response = self.nlp_processor.generate_response(text, intent, sentiment)
            return response
        except Exception as e:
            logging.error(f"Error in process_input: {str(e)}")
            return "Maaf, terjadi kesalahan dalam memproses permintaan Anda."

    def run(self):
        welcome_message = "Halo! Saya asisten fashion Anda. Apa jenis pakaian yang Anda cari?"
        print("\n" + "="*50)
        print("Fashion Chatbot Indonesia")
        print("Katakan 'keluar' untuk mengakhiri percakapan")
        print("="*50 + "\n")

        self.text_to_speech(welcome_message)

        while True:
            user_input = self.speech_to_text()
            if not user_input:
                continue
            response = self.process_input(user_input)
            if response == "KELUAR":
                farewell = "Terima kasih telah menggunakan Fashion Chatbot. Sampai jumpa!"
                self.text_to_speech(farewell)
                break
            self.text_to_speech(response)

if __name__ == "__main__":
    chatbot = AzureFashionChatbot()
    chatbot.run()
