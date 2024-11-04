# src/chatbot.py
import speech_recognition as sr
import pyttsx3

class FashionChatbotID:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()

        voices = self.tts_engine.getProperty('voices')
        for voice in voices:
            if "indonesia" in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break

        self.tts_engine.setProperty('rate', 160)
        self.tts_engine.setProperty('volume', 0.9)

    def speech_to_text(self):
        """Konversi suara ke teks dalam Bahasa Indonesia"""
        with sr.Microphone() as source:
            print("Mendengarkan...")
            try:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio, language="id-ID")
                print(f"Anda mengatakan: {text}")
                return text.lower()
            except sr.UnknownValueError:
                print("Maaf, saya tidak dapat mendengar dengan jelas")
                return ""
            except sr.RequestError as e:
                print(f"Terjadi kesalahan pada layanan speech recognition; {e}")
                return ""
            except Exception as e:
                print(f"Error: {e}")
                return ""

    def text_to_speech(self, text):
        """Konversi teks ke suara dalam Bahasa Indonesia"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Error TTS: {e}")

    def get_fashion_response(self, text):
        """Generate respons berdasarkan input pengguna"""
        fashion_responses = {
            "formal": {
                "pria": [
                    "Untuk acara formal, saya sarankan kemeja putih lengan panjang dengan celana bahan hitam dan sepatu pantofel.",
                    "Anda bisa mengenakan setelan jas navy blue dengan kemeja putih dan dasi senada.",
                    "Kombinasi kemeja light blue dengan celana bahan gelap akan cocok untuk acara formal."
                ],
                "wanita": [
                    "Untuk acara formal, saya sarankan blazer dengan rok pensil atau celana bahan.",
                    "Dress hitam formal dengan panjang selutut akan terlihat sangat profesional.",
                    "Blus formal dengan celana bahan atau rok midi akan cocok untuk acara formal."
                ]
            },
            "kasual": {
                "pria": [
                    "Untuk gaya kasual, coba padukan kaos polos dengan celana jeans dan sneakers.",
                    "Kemeja casual lengan pendek dengan chinos dan loafers bisa jadi pilihan santai yang tetap stylish.",
                    "Polo shirt dengan celana chinos dan sneakers putih akan memberikan tampilan smart casual."
                ],
                "wanita": [
                    "Untuk gaya kasual, blus santai dengan celana jeans dan flat shoes akan terlihat cantik.",
                    "Dress casual dengan sneakers bisa jadi pilihan nyaman untuk kegiatan sehari-hari.",
                    "Kaos oversized dengan celana kulot dan sandals akan memberikan tampilan santai yang tetap modis."
                ]
            }
        }

        style = "kasual"
        gender = "pria"

        if any(word in text for word in ["formal", "resmi", "kerja", "kantor", "meeting"]):
            style = "formal"
        if any(word in text for word in ["santai", "casual", "kasual"]):
            style = "kasual"
        if any(word in text for word in ["wanita", "cewek", "perempuan"]):
            gender = "wanita"

        import random
        return random.choice(fashion_responses[style][gender])

    def analyze_input(self, text):
        """Analisis input pengguna untuk menentukan respons yang tepat"""
        if not text:
            return "Maaf, bisakah Anda mengulangi apa yang Anda katakan?"

        if any(word in text for word in ["keluar", "selesai", "quit", "exit", "stop"]):
            return "KELUAR"

        if any(word in text for word in ["hai", "halo", "hi", "hello"]):
            return "Halo! Saya asisten fashion Anda. Apakah Anda mencari pakaian formal atau kasual?"

        return self.get_fashion_response(text)

    def run(self):
        """Jalankan chatbot"""
        welcome_message = "Halo! Saya asisten fashion Anda. Apa jenis pakaian yang Anda cari? Formal atau kasual?"
        print("\n" + "="*50)
        print("Fashion Chatbot Indonesia")
        print("Katakan 'keluar' untuk mengakhiri percakapan")
        print("="*50 + "\n")

        print("Asisten: " + welcome_message)
        self.text_to_speech(welcome_message)

        while True:
            user_input = self.speech_to_text()

            if not user_input:
                continue

            response = self.analyze_input(user_input)

            if response == "KELUAR":
                farewell = "Terima kasih telah menggunakan Fashion Chatbot. Sampai jumpa!"
                print("Asisten: " + farewell)
                self.text_to_speech(farewell)
                break

            print("Asisten: " + response)
            self.text_to_speech(response)

if __name__ == "__main__":
    chatbot = FashionChatbotID()
    chatbot.run()