# 2️⃣ Capture and transcribe voice input
import streamlit as st
from openai import OpenAI
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import io

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def record_audio(duration=5, fs=44100):
    st.info("🎙️ Recording... Speak now!")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    wav_io = io.BytesIO()
    write(wav_io, fs, recording)
    wav_io.seek(0)
    return wav_io

# 3️⃣ Convert audio → text (Speech-to-Text)
def transcribe_audio(audio_bytes):
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=("input.wav", audio_bytes)
    )
    return transcription.text

# 4️⃣ Send that text to your same chat logic
def get_ai_response(user_text, recruiter_intro, resume_text):
    prompt = f"""
    You are an AI Career Assistant representing Nagaphani Buddepu...
    Recruiter said: "{recruiter_intro}"
    Question: {user_text}
    Résumé: {resume_text}
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 5️⃣ Convert text → speech
def speak_response(text):
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",  # options: alloy, verse, coral, etc.
        input=text
    )
    audio_bytes = speech.read()
    st.audio(audio_bytes, format="audio/mp3")

# 6️⃣ Combine all in Streamlit UI
st.title("🎙️ Voice Chat with Nagaphani’s AI Career Assistant")

if st.button("🎧 Record Question"):
    audio_data = record_audio(duration=6)
    user_text = transcribe_audio(audio_data)
    st.write("🗣️ You said:", user_text)

    response_text = get_ai_response(user_text, recruiter_intro="", resume_text="(your resume text)")
    st.write("🤖 AI:", response_text)

    speak_response(response_text)

