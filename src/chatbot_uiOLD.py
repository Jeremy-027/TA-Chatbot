# src/chatbot_ui.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from chatbot_azure import AzureFashionChatbot
import os


class FashionChatbotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fashion Chatbot Indonesia")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Initialize chatbot (will be done when start is clicked)
        self.chatbot = None
        self.is_listening = False
        self.conversation_active = False

        # Configure style
        self.setup_styles()

        # Create UI elements
        self.create_widgets()

        # Center the window
        self.center_window()

    def setup_styles(self):
        """Setup custom styles for the UI"""
        style = ttk.Style()
        style.theme_use("clam")

        # Configure custom styles
        style.configure("Title.TLabel", font=("Arial", 16, "bold"))
        style.configure("Subtitle.TLabel", font=("Arial", 10))
        style.configure("Status.TLabel", font=("Arial", 9), foreground="blue")
        style.configure("Start.TButton", font=("Arial", 12, "bold"))
        style.configure("Action.TButton", font=("Arial", 10))

    def create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame, text="Fashion Chatbot Indonesia", style="Title.TLabel"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        subtitle_label = ttk.Label(
            main_frame,
            text="Asisten Fashion Berbahasa Indonesia dengan Voice Recognition",
            style="Subtitle.TLabel",
        )
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))

        # Control buttons frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(
            row=2, column=0, columnspan=3, pady=(0, 20), sticky=(tk.W, tk.E)
        )
        control_frame.columnconfigure(1, weight=1)

        # Start/Stop button
        self.start_button = ttk.Button(
            control_frame,
            text="Mulai Chatbot",
            command=self.toggle_chatbot,
            style="Start.TButton",
        )
        self.start_button.grid(row=0, column=0, padx=(0, 10))

        # Listen button
        self.listen_button = ttk.Button(
            control_frame,
            text="🎤 Dengarkan",
            command=self.start_listening,
            style="Action.TButton",
            state="disabled",
        )
        self.listen_button.grid(row=0, column=1, padx=(0, 10))

        # Stop conversation button
        self.stop_button = ttk.Button(
            control_frame,
            text="Akhiri Percakapan",
            command=self.stop_conversation,
            style="Action.TButton",
            state="disabled",
        )
        self.stop_button.grid(row=0, column=2)

        # Status label
        self.status_label = ttk.Label(
            main_frame, text="Klik 'Mulai Chatbot' untuk memulai", style="Status.TLabel"
        )
        self.status_label.grid(row=3, column=0, columnspan=3, pady=(0, 10))

        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.grid(
            row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10)
        )

        # Speech Input Tab
        input_frame = ttk.Frame(notebook)
        notebook.add(input_frame, text="Input Suara")

        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(1, weight=1)

        ttk.Label(
            input_frame, text="Apa yang Anda katakan:", font=("Arial", 10, "bold")
        ).grid(row=0, column=0, sticky=tk.W, padx=10, pady=(10, 5))

        self.input_text = scrolledtext.ScrolledText(
            input_frame, height=8, wrap=tk.WORD, font=("Arial", 10)
        )
        self.input_text.grid(
            row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=(0, 10)
        )
        self.input_text.config(state="disabled")

        # Response Tab
        response_frame = ttk.Frame(notebook)
        notebook.add(response_frame, text="Rekomendasi Fashion")

        response_frame.columnconfigure(0, weight=1)
        response_frame.rowconfigure(1, weight=1)

        ttk.Label(
            response_frame, text="Rekomendasi Asisten:", font=("Arial", 10, "bold")
        ).grid(row=0, column=0, sticky=tk.W, padx=10, pady=(10, 5))

        self.response_text = scrolledtext.ScrolledText(
            response_frame, height=8, wrap=tk.WORD, font=("Arial", 10)
        )
        self.response_text.grid(
            row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=(0, 10)
        )
        self.response_text.config(state="disabled")

        # Conversation History Tab
        history_frame = ttk.Frame(notebook)
        notebook.add(history_frame, text="Riwayat Percakapan")

        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(1, weight=1)

        ttk.Label(
            history_frame, text="Riwayat Lengkap:", font=("Arial", 10, "bold")
        ).grid(row=0, column=0, sticky=tk.W, padx=10, pady=(10, 5))

        self.history_text = scrolledtext.ScrolledText(
            history_frame, height=8, wrap=tk.WORD, font=("Arial", 9)
        )
        self.history_text.grid(
            row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=(0, 10)
        )
        self.history_text.config(state="disabled")

        # Clear history button
        clear_button = ttk.Button(
            history_frame, text="Bersihkan Riwayat", command=self.clear_history
        )
        clear_button.grid(row=2, column=0, pady=(0, 10))

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def toggle_chatbot(self):
        """Start or stop the chatbot"""
        if not self.conversation_active:
            self.start_chatbot()
        else:
            self.stop_chatbot()

    def start_chatbot(self):
        """Initialize and start the chatbot"""
        try:
            self.update_status("Menginisialisasi chatbot...")
            self.start_button.config(state="disabled")

            # Initialize chatbot in a separate thread to prevent UI freezing
            def init_chatbot():
                try:
                    self.chatbot = AzureFashionChatbot()
                    self.conversation_active = True

                    # Update UI in main thread
                    self.root.after(0, self.on_chatbot_started)

                except Exception as e:
                    error_msg = f"Error menginisialisasi chatbot: {str(e)}"
                    self.root.after(0, lambda: self.show_error(error_msg))

            threading.Thread(target=init_chatbot, daemon=True).start()

        except Exception as e:
            self.show_error(f"Error: {str(e)}")

    def on_chatbot_started(self):
        """Called when chatbot is successfully started"""
        self.update_status("Chatbot siap! Klik 'Dengarkan' untuk mulai berbicara.")
        self.start_button.config(text="Hentikan Chatbot", state="normal")
        self.listen_button.config(state="normal")
        self.stop_button.config(state="normal")

        # Add welcome message
        welcome_msg = (
            "Halo! Saya asisten fashion Anda. Apa jenis pakaian yang Anda cari?"
        )
        self.add_to_response(welcome_msg)
        self.add_to_history("Asisten", welcome_msg)

        # Use text-to-speech for welcome message
        if self.chatbot:
            threading.Thread(
                target=lambda: self.chatbot.text_to_speech(welcome_msg), daemon=True
            ).start()

    def stop_chatbot(self):
        """Stop the chatbot"""
        self.conversation_active = False
        self.is_listening = False
        self.chatbot = None

        self.start_button.config(text="Mulai Chatbot", state="normal")
        self.listen_button.config(state="disabled")
        self.stop_button.config(state="disabled")
        self.update_status(
            "Chatbot dihentikan. Klik 'Mulai Chatbot' untuk memulai lagi."
        )

    def start_listening(self):
        """Start listening for speech input"""
        if not self.chatbot or self.is_listening:
            return

        self.is_listening = True
        self.listen_button.config(state="disabled", text="🎤 Mendengarkan...")
        self.update_status("Mendengarkan... Silakan berbicara.")

        def listen():
            try:
                # Get speech input
                user_input = self.chatbot.speech_to_text()

                if user_input:
                    # Update UI with user input
                    self.root.after(0, lambda: self.add_to_input(user_input))
                    self.root.after(0, lambda: self.add_to_history("Anda", user_input))

                    # Process the input
                    response, is_error, clothing_json = self.chatbot.process_input(
                        user_input
                    )

                    # Check if user wants to exit
                    if response == "KELUAR":
                        farewell = "Terima kasih telah menggunakan Fashion Chatbot. Sampai jumpa!"
                        self.root.after(0, lambda: self.add_to_response(farewell))
                        self.root.after(
                            0, lambda: self.add_to_history("Asisten", farewell)
                        )
                        self.chatbot.text_to_speech(farewell)
                        self.root.after(0, self.stop_conversation)
                        return

                    # Update UI with response
                    self.root.after(0, lambda: self.add_to_response(response))
                    self.root.after(0, lambda: self.add_to_history("Asisten", response))

                    # Speak the response (don't speak error messages)
                    if not is_error:
                        self.chatbot.text_to_speech(response)

                else:
                    self.root.after(
                        0,
                        lambda: self.update_status(
                            "Tidak dapat mengenali suara. Coba lagi."
                        ),
                    )

            except Exception as e:
                error_msg = f"Error dalam mendengarkan: {str(e)}"
                self.root.after(0, lambda: self.show_error(error_msg))

            finally:
                # Re-enable listen button
                self.root.after(0, self.on_listening_finished)

        threading.Thread(target=listen, daemon=True).start()

    def on_listening_finished(self):
        """Called when listening is finished"""
        self.is_listening = False
        if self.conversation_active:
            self.listen_button.config(state="normal", text="🎤 Dengarkan")
            self.update_status(
                "Siap mendengarkan. Klik 'Dengarkan' untuk berbicara lagi."
            )

    def stop_conversation(self):
        """Stop the current conversation"""
        self.stop_chatbot()
        self.add_to_response("Percakapan diakhiri.")
        self.add_to_history("Sistem", "Percakapan diakhiri.")

    def add_to_input(self, text):
        """Add text to input display"""
        self.input_text.config(state="normal")
        self.input_text.insert(tk.END, f"{text}\n\n")
        self.input_text.see(tk.END)
        self.input_text.config(state="disabled")

    def add_to_response(self, text):
        """Add text to response display"""
        self.response_text.config(state="normal")
        self.response_text.insert(tk.END, f"{text}\n\n")
        self.response_text.see(tk.END)
        self.response_text.config(state="disabled")

    def add_to_history(self, speaker, text):
        """Add to conversation history"""
        self.history_text.config(state="normal")
        self.history_text.insert(tk.END, f"[{speaker}]: {text}\n\n")
        self.history_text.see(tk.END)
        self.history_text.config(state="disabled")

    def clear_history(self):
        """Clear conversation history"""
        self.history_text.config(state="normal")
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state="disabled")

        self.input_text.config(state="normal")
        self.input_text.delete(1.0, tk.END)
        self.input_text.config(state="disabled")

        self.response_text.config(state="normal")
        self.response_text.delete(1.0, tk.END)
        self.response_text.config(state="disabled")

    def update_status(self, message):
        """Update status label"""
        self.status_label.config(text=message)

    def show_error(self, message):
        """Show error message"""
        self.update_status(f"Error: {message}")
        messagebox.showerror("Error", message)
        self.start_button.config(state="normal")

    def on_closing(self):
        """Handle window closing"""
        if self.conversation_active:
            if messagebox.askokcancel("Keluar", "Apakah Anda yakin ingin keluar?"):
                self.stop_chatbot()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    if not os.getenv("AZURE_SPEECH_KEY") or not os.getenv("AZURE_SPEECH_REGION"):
        messagebox.showerror(
            "Konfigurasi Error",
            "Azure Speech credentials tidak ditemukan!\n\n"
            "Pastikan file .env berisi:\n"
            "AZURE_SPEECH_KEY=your_key_here\n"
            "AZURE_SPEECH_REGION=your_region_here",
        )
        return

    root = tk.Tk()
    app = FashionChatbotUI(root)

    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)

    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main()
