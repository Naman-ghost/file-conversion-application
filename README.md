# 📁 File Conversion Application

A multi-functional utility that lets users convert PDFs to customizable DOCX files and transcribe voice to text — all with a sleek GUI.

---

## 🔧 Features

- 📄 **PDF to DOCX Converter**
  - Customize **font style** and **text size**
  - Converts while preserving layout and formatting
- 🎙️ **Voice to Text**
  - Converts audio files (.wav, .mp3) to plain text
  - Accurate transcription using SpeechRecognition
- 🖼️ Clean, responsive GUI built with Tkinter
- 🧵 Runs long tasks on separate threads to avoid UI freezing

---

## 🛠 Tech Stack

- **Python**
  - `pdf2docx` – PDF to DOCX conversion
  - `docx` – Custom DOCX generation
  - `speech_recognition` – Audio transcription
  - `Pillow` – Image support in Tkinter GUI
  - `sqlite3` – (optional) for session data or logs
  - `threading` – for non-blocking background tasks
  - `Tkinter` – GUI development

---

## 🚀 How to Run

```bash
git clone https://github.com/your-username/file-conversion-application.git
cd file-conversion-app
python app.py
