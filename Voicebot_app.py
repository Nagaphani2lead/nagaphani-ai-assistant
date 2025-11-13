import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import requests
from io import BytesIO
import sounddevice as sd
import numpy as np
import wavio

# -------------------- SETUP --------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

RESUME_VIEW_URL = "https://drive.google.com/file/d/1A9fGkLL-oP9LbPNWLsWjevBzHb5Qx3Ki/view?usp=sharing"
RESUME_DOWNLOAD_URL = "https://drive.google.com/uc?id=1A9fGkLL-oP9LbPNWLsWjevBzHb5Qx3Ki"
PHONE = "+91-7304060673"
EMAIL = "nagaphani.leads@gmail.com"
QR_IMAGE_PATH = "Nagaphani_Buddepu_QR_Stylish.png"


# -------------------- LOAD RESUME TEXT --------------------
try:
    response = requests.get(RESUME_DOWNLOAD_URL)
    pdf = BytesIO(response.content)
    reader = PdfReader(pdf)
    resume_text = "".join([page.extract_text() or "" for page in reader.pages])
    resume_text = resume_text[:15000]
except:
    resume_text = "Resume could not be loaded."


# -------------------- STREAMLIT UI --------------------
st.set_page_config(page_title="Voice Chat with Nagaphani", page_icon="🎤")
st.title("🎤 Nagaphani’s AI Career Voice Assistant")
st.caption("Ask about my experience, projects, certifications, or résumé.")

st.divider()

# -------------------- RECRUITER INTRO --------------------
st.markdown("👋 **Hi, I’m Nagaphani’s AI Career Assistant (Voice Mode).**")
st.write("Before we talk, could you please tell me a bit about the position or company you're hiring for?")

recruiter_intro = st.text_area("Company / Position Details:", "")
if recruiter_intro.strip():
    st.success("Perfect. You can now speak your questions.")
else:
    st.info("Please fill the recruiter details before asking questions.")


# -------------------- RECORD AUDIO --------------------
def record_audio(duration=5, fs=44100):
    st.info("🎧 Listening... speak now.")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    return audio, fs


# -------------------- BUTTON --------------------
if st.button("🎙️ Tap to Speak"):
    if not recruiter_intro.strip():
        st.warning("Please enter recruiter/company details first.")
        st.stop()

    # Record
    audio, fs = record_audio()
    wavio.write("input.wav", audio, fs, sampwidth=2)
    st.success("Audio captured.")

    # Speech → Text
    with open("input.wav", "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=f
        )
    user_text = transcript.text
    st.write("🗣️ **You said:**", user_text)

    # -------------------- CONTACT INFO HANDLING --------------------
    keywords = ["contact", "phone", "email", "linkedin", "resume", "qr", "download", "pdf"]
    if any(k in user_text.lower() for k in keywords):
        st.subheader("📞 Contact Details")
        st.markdown(f"""
        - **Phone:** {PHONE}  
        - **Email:** [{EMAIL}](mailto:{EMAIL})  
        - **LinkedIn:** https://www.linkedin.com/in/phani2lead/  
        - **Résumé:** [View PDF]({RESUME_VIEW_URL})
        """)
        try:
            st.image(QR_IMAGE_PATH, width=180)
        except:
            pass

        # Audio response
        reply_text = f"My contact details are: Phone {PHONE}, Email {EMAIL}, and LinkedIn phani2lead."
    else:
        # -------------------- PROFESSIONAL CONTEXT --------------------
        extra_context = """
        Nagaphani Buddepu is currently available for immediate joining.
        He has deep experience in AI Delivery, Digital Transformation,
        Agile/DevOps/MLOps coaching, ISO compliance, and Enterprise leadership.

        He mentors early-stage founders, students, and enterprises.
        Ideal roles: Head of AI Delivery, AI Transformation Leader,
        Enterprise AI Program Director, Chief Digital & AI Officer.

        Current CTC ~55 LPA, expected 80 LPA – 1 Cr depending on scope.
        """

        # -------------------- SAME SYSTEM PROMPT (from chatbot) --------------------
        full_prompt = f"""
        You are an AI Career Assistant representing Nagaphani Buddepu.
        This conversation is with a recruiter who shared this about the role:
        "{recruiter_intro}"

        Use both the résumé and the professional context below to answer clearly,
        confidently and in a recruiter-friendly tone. Highlight leadership,
        transformation, and AI delivery strengths.

        If a question isn’t covered in the résumé/context, reply with:
        "That topic isn't mentioned in my résumé, but I'd be happy to discuss it further."

        Professional Context:
        {extra_context}

        Résumé:
        {resume_text}

        Recruiter question:
        {user_text}
        """

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": full_prompt}],
        )
        reply_text = completion.choices[0].message.content
        st.write("🤖 **AI Assistant:**", reply_text)

    # Text → Speech
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=reply_text
    )

    with open("reply.wav", "wb") as f:
        f.write(speech.read())

    st.audio("reply.wav")
