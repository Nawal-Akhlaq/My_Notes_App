# YouTube-to-Notes & Text Processing App

## Overview
This AI-powered web application automates transcription, summarization, translation, text-to-speech conversion, and document export—all in one place. Whether you want to extract insights from YouTube videos, summarize lengthy text, or convert notes into speech, this tool has got you covered!

## Features
- 🎥 **YouTube Video Transcription**: Extracts audio from YouTube videos and converts speech to text using **Whisper AI**.
- 📝 **Summarization**: Generates concise summaries of text using **Facebook’s BART model**.
- 🌍 **Translation**: Supports multilingual translation with **Google Translate API**.
- 🔊 **Text-to-Speech (TTS)**: Converts text into natural-sounding speech using **gTTS**.
- 📄 **Export Options**: Save your processed text as **PDF** or **Word (DOCX)** files.
- 🖥️ **User-Friendly Web Interface**: Built with **Gradio** for an interactive UI.

## Technologies Used
- **Python**
- **Whisper AI (Faster-Whisper)** for speech-to-text conversion
- **Hugging Face Transformers (BART Summarization)**
- **Google Translator API** for translations
- **gTTS (Google Text-to-Speech)**
- **yt-dlp** for YouTube audio extraction
- **FPDF & python-docx** for document generation
- **Gradio** for UI development

## Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/MY_Notes_APP.git
   cd MY_Notes_APP
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Authenticate Hugging Face (Optional):**
   ```python
   from huggingface_hub import login
   login("your_huggingface_token")
   ```
4. **Run the application:**
   ```sh
   python app.py
   ```

## Usage
- **YouTube to Notes:** Paste a YouTube URL and get the transcription + summary.
- **Notes Processor:** Input text and choose an action (Summarize, Translate, TTS, Export as PDF/Word).
- **Download Results:** Save processed text/audio for future use.

## Contributions
Contributions are welcome! Feel free to open an issue or submit a pull request.

## Acknowledgments
Special thanks to the **open-source community** for providing the amazing libraries that power this application!

---
🚀 **Try it out and make content consumption easier!**
