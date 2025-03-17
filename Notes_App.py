#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import yt_dlp
import gradio as gr
from faster_whisper import WhisperModel
from gtts import gTTS
from deep_translator import GoogleTranslator
from fpdf import FPDF
from docx import Document
from transformers import pipeline
from huggingface_hub import login

# Authenticate Hugging Face
login("YOUR_HUGGING_FACE_TOKEN")

# Setup directories
UPLOAD_PATH = "uploads"
os.makedirs(UPLOAD_PATH, exist_ok=True)

# Initialize models
model = WhisperModel("base", compute_type="float32")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def download_audio(video_url):
    """Download audio from YouTube."""
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
            'outtmpl': os.path.join(UPLOAD_PATH, "%(title)s.%(ext)s"),
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            audio_filename = ydl.prepare_filename(info_dict).replace(".webm", ".mp3").replace(".m4a", ".mp3")
        return audio_filename
    except Exception as e:
        return f"Error downloading audio: {str(e)}"

def transcribe_audio(audio_path):
    """Transcribe audio using Whisper AI."""
    try:
        if not os.path.exists(audio_path):
            return f"Error: File {audio_path} not found."
        segments, _ = model.transcribe(audio_path)
        return " ".join(segment.text for segment in segments)
    except Exception as e:
        return f"Transcription error: {str(e)}"

def chunk_text(text, chunk_size=800):
    """Splits text into smaller chunks."""
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def summarize_text(text):
    """Summarizes text in chunks."""
    try:
        if len(text.split()) < 30:
            return "Error: Text too short for summarization."
        text_chunks = chunk_text(text, chunk_size=400)
        summaries = [summarizer(chunk, max_length=150, min_length=50, do_sample=False)[0]['summary_text'] for chunk in text_chunks]
        return " ".join(summaries)
    except Exception as e:
        return f"Summarization error: {str(e)}"

def text_to_speech(text, lang="en"):
    """Convert text to speech."""
    try:
        tts_path = os.path.join(UPLOAD_PATH, "note_audio.mp3")
        gTTS(text=text, lang=lang).save(tts_path)
        return tts_path if os.path.exists(tts_path) else "Error: TTS failed."
    except Exception as e:
        return f"TTS error: {str(e)}"

def translate_text(text, target_lang):
    """Translate text."""
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        return f"Translation error: {str(e)}"

def export_pdf(text, filename="note.pdf"):
    """Export text to a PDF file."""
    try:
        pdf_path = os.path.join(UPLOAD_PATH, filename)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text)
        pdf.output(pdf_path)
        return pdf_path
    except Exception as e:
        return f"PDF export error: {str(e)}"

def export_word(text, filename="note.docx"):
    """Export text to a Word document."""
    try:
        word_path = os.path.join(UPLOAD_PATH, filename)
        doc = Document()
        doc.add_paragraph(text)
        doc.save(word_path)
        return word_path
    except Exception as e:
        return f"Word export error: {str(e)}"

def process_video(video_url):
    """Process YouTube video: Download, transcribe, summarize."""
    audio_path = download_audio(video_url)
    if "Error" in audio_path:
        return audio_path, ""
    transcription = transcribe_audio(audio_path)
    summary = summarize_text(transcription)
    os.remove(audio_path)  # Cleanup
    return transcription, summary

def note_app(note_text, action, language="en"):
    """Perform actions on text notes."""
    if action == "Summarize":
        return summarize_text(note_text), None
    elif action == "Translate":
        return translate_text(note_text, language), None
    elif action == "Text-to-Speech":
        tts_path = text_to_speech(note_text, language)
        return "Audio generated successfully. Download below.", tts_path
    elif action == "Export as PDF":
        return "PDF generated successfully. Download below.", export_pdf(note_text)
    elif action == "Export as Word":
        return "Word document generated successfully. Download below.", export_word(note_text)
    return "Invalid Action", None

# Gradio UI
with gr.Blocks() as app:
    with gr.Tab("YouTube to Notes"):
        video_url = gr.Textbox(label="YouTube Video URL")
        transcription = gr.Textbox(label="Transcription", interactive=False)
        summary = gr.Textbox(label="Summary", interactive=False)
        btn_transcribe = gr.Button("Transcribe & Summarize")
        btn_transcribe.click(process_video, inputs=video_url, outputs=[transcription, summary])
    
    with gr.Tab("Notes Processor"):
        note_text = gr.Textbox(label="Enter your note")
        action = gr.Radio(["Summarize", "Translate", "Text-to-Speech", "Export as PDF", "Export as Word"], label="Choose an action")
        language = gr.Textbox(label="Language (for translation/TTS, e.g., 'en', 'es')", value="en")
        result = gr.Textbox(label="Result", interactive=False)
        file_output = gr.File(label="Download File")
        btn_process = gr.Button("Process Note")
        btn_process.click(note_app, inputs=[note_text, action, language], outputs=[result, file_output])


app.launch(share=False)
