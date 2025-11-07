pip install openai streamlit sounddevice numpy scipy

import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import requests
from io import BytesIO
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import io

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="🎙️ Voice Chat with Nagaphani", page_icon="🎧")

# -------------------- SETUP --------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Resume link (Google Drive)
RESUME_DOWNLOAD_URL = "https://drive.google.com/uc?id=1A9fGkLL-oP9LbPNWLsWjevBzHb5Qx3Ki"

# -------------------- LOAD RESUME --------------------
@st.cache_data(show_spinner=False)
def load_resume_text():
    try:
        response = requests.get(RESUME_DOWNLOAD_URL)
        pdf = BytesIO(response.content)
        reader = PdfReader(pdf)
        text = "".join([page.extract_text() or "" for page in reader.pages])
        return text[:15000]
    except Exception as e:
        st.error(f"Error reading resume: {e}")
        return "Resume could not be loaded."
        
resume_text = load_resume_text()

# -------------------- AUDIO RECORDING --------------------
def record_audio(duration=5, fs=44100):
    st.info("🎙️ Recording... Please speak now!")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype="int16")
    sd.wait()
    wav_io = io.BytesIO()
    write(wav_io, fs, recording)
    wav_io.seek(0)
    st.success("✅ Recording finished.")
    return wav_io

# -------------------- AUDIO → TEXT --------------------
def transcribe_audio(audio_bytes):
    st.info("🎧 Transcribing your question...")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=("input.wav", audio_bytes)
    )
    return transcription.text

# -------------------- GET GPT RESPONSE --------------------
def get_ai_response(user_text, resume_text):
    prompt = f"""
    You are an AI Career Assistant representing Nagaphani Buddepu.
    The recruiter asked: "{user_text}"

    Use the résumé and context below to answer confidently and professionally.
    If a topic isn't mentioned, respond gracefully with:
    "That topic isn't mentioned in my résumé, but I'd be happy to discuss it further."

    Résumé:
    {resume_text}
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

# -------------------- TEXT → SPEECH --------------------
def speak_response(text):
    st.info("🔊 Generating voice response...")
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",  # Voices: alloy, verse, coral, sage
        input=text
    )
    audio_bytes = speech.read()
    st.audio(audio_bytes, format="audio/mp3")

# -------------------- UI --------------------
st.markdown("## 🎙️ Talk with Nagaphani’s AI Career Assistant")
st.caption("Ask about experience, leadership, or certifications — now via voice!")

duration = st.slider("Select recording duration (seconds)", 3, 10, 5)

if st.button("🎤 Record Question"):
    audio_data = record_audio(duration)
    user_text = transcribe_audio(audio_data)
    st.write("🗣️ You said:", user_text)

    with st.spinner("🤖 Thinking..."):
        response_text = get_ai_response(user_text, resume_text)
        st.write("**AI:**", response_text)
        speak_response(response_text)

st.markdown("---")
st.caption("🤖 Designed by Nagaphani Buddepu | Voice-Enabled Career Assistant | AI Delivery • Product Leadership • Transformation Excellence")
