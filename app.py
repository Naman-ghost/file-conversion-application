import os
import sqlite3
import threading
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from pdf2docx import Converter
from docx import Document
import speech_recognition as sr
from PIL import Image, ImageTk

app = Tk()
app.title("Smart File Converter")
app.geometry("1000x800")
app.configure(bg="#f5f7fa")

DB_FILE = "conversion_reviews.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            review TEXT,
            stars INTEGER
        )
    """)
    conn.commit()
    conn.close()

init_db()

def log_review(username, review, stars):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO reviews (username, review, stars) VALUES (?, ?, ?)", (username, review, stars))
    conn.commit()
    conn.close()

def fetch_reviews():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT username, review, stars FROM reviews")
    reviews = cur.fetchall()
    conn.close()
    return reviews

def convert_pdf_to_docx(files):
    for file_path in files:
        if file_path.endswith(".pdf"):
            filename = os.path.splitext(os.path.basename(file_path))[0]
            output_path = os.path.join("outputs", f"{filename}.docx")
            cv = Converter(file_path)
            cv.convert(output_path, start=0, end=None)
            cv.close()
            log_text.insert(END, f"✅ Converted: {filename}.pdf → {filename}.docx\n")
            log_text.see(END)

def convert_audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        log_text.insert(END, f"🎧 Audio Text: {text}\n")
        log_text.see(END)
    except:
        log_text.insert(END, "Could not recognize audio\n")

live_text = ""
listening = False

def start_listening():
    global listening, live_text
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    listening = True
    live_text = ""

    def listen():
        nonlocal recognizer, mic
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            while listening:
                try:
                    audio = recognizer.listen(source, timeout=5)
                    text = recognizer.recognize_google(audio)
                    live_text += " " + text
                    live_output.config(state=NORMAL)
                    live_output.delete(1.0, END)
                    live_output.insert(END, live_text.strip())
                    live_output.config(state=DISABLED)
                except:
                    continue

    threading.Thread(target=listen).start()

def stop_listening():
    global listening
    listening = False
    log_text.insert(END, f"🗣️ Final Live Text: {live_text.strip()}\n")
    log_text.see(END)

def reset_live_text():
    global live_text
    live_text = ""
    live_output.config(state=NORMAL)
    live_output.delete(1.0, END)
    live_output.config(state=DISABLED)


def submit_review():
    username = review_user.get().strip()
    review = review_entry.get().strip()
    stars = star_var.get()
    if username and review:
        log_review(username, review, stars)
        messagebox.showinfo("Thank You!", "🌟 Your review has been submitted!")
        review_user.delete(0, END)
        review_entry.delete(0, END)
        star_var.set(5)
        load_reviews()

def load_reviews():
    reviews = fetch_reviews()
    log_text.insert(END, "\n🦡 User Reviews:\n")
    for user, review, stars in reviews:
        log_text.insert(END, f"{'⭐' * stars} {user}: {review}\n")
    log_text.insert(END, "-" * 60 + "\n")
    log_text.see(END)


title = Label(app, text="🌈 Smart File Converter", font=("Helvetica", 24, "bold"), bg="#f5f7fa", fg="#4b0082")
title.pack(pady=(10, 5))

pdf_frame = LabelFrame(app, text="📄 PDF to DOCX Converter", bg="#f0fff0", font=("Arial", 12, "bold"), padx=10, pady=10)
pdf_frame.pack(fill="x", padx=30, pady=(10, 5))

def select_pdfs():
    files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    if files:
        convert_pdf_to_docx(files)

pdf_btn = ttk.Button(pdf_frame, text="🗂 Select PDF Files", command=select_pdfs)
pdf_btn.pack(pady=5)

button_frame = Frame(app, bg="#f5f7fa")
button_frame.pack(pady=10)

def select_audio():
    file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
    if file:
        convert_audio_to_text(file)

ttk.Button(button_frame, text="🎧 Audio to Text", command=select_audio).grid(row=0, column=0, padx=10)
ttk.Button(button_frame, text="▶️ Start Live Speech", command=start_listening).grid(row=0, column=1, padx=10)
ttk.Button(button_frame, text="⏹ Stop", command=stop_listening).grid(row=0, column=2, padx=10)
ttk.Button(button_frame, text="🔁 Reset Text", command=reset_live_text).grid(row=0, column=3, padx=10)

live_output = Text(app, height=4, width=100, state=DISABLED, bg="#fff0f5", font=("Arial", 12))
live_output.pack(pady=10)

review_frame = LabelFrame(app, text="🗣️ Leave a Review", bg="#fafafa", font=("Arial", 12, "bold"))
review_frame.pack(padx=20, pady=15, fill="x")

Label(review_frame, text="Name:", bg="#fafafa").grid(row=0, column=0, sticky=W, padx=5, pady=5)
review_user = Entry(review_frame)
review_user.grid(row=0, column=1, padx=5, pady=5)

Label(review_frame, text="Your Review:", bg="#fafafa").grid(row=1, column=0, sticky=W, padx=5)
review_entry = Entry(review_frame, width=60)
review_entry.grid(row=1, column=1, padx=5, pady=5)

Label(review_frame, text="Rating:", bg="#fafafa").grid(row=2, column=0, sticky=W, padx=5)
star_var = IntVar(value=5)
star_frame = Frame(review_frame, bg="#fafafa")
star_frame.grid(row=2, column=1, sticky=W)

for i in range(1, 6):
    Radiobutton(star_frame, text="⭐", variable=star_var, value=i, bg="#fafafa").pack(side=LEFT)

ttk.Button(review_frame, text="📨 Submit Review", command=submit_review).grid(row=3, column=0, columnspan=2, pady=5)

log_text = Text(app, height=12, width=105, bg="#e8f0fe", font=("Courier", 11))
log_text.pack(pady=15)
log_text.insert(END, "📋 App Started. Ready to convert!\n")
log_text.config(state=NORMAL)

os.makedirs("outputs", exist_ok=True)

load_reviews()
app.mainloop()