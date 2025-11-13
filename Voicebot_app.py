import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import requests
from io import BytesIO

# -------------------- SETUP --------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

RESUME_VIEW_URL = "https://drive.google.com/file/d/1A9fGkLL-oP9LbPNWLsWjevBzHb5Qx3Ki/view?usp=sharing"
RESUME_DOWNLOAD_URL = "https://drive.google.com/uc?id=1A9fGkLL-oP9LbPNWLsWjevBzHb5Qx3Ki"
PHONE = "+91-7304060673"
EMAIL = "nagaphani.leads@gmail.com"
QR_IMAGE_PATH = "Nagaphani_Buddepu_QR_Stylish.png"


# -------------------- LOAD RESUME TEXT --------------------
@st.cache_data
def load_resume_text():
    try:
        response = requests.get(RESUME_DOWNLOAD_URL)
        pdf = BytesIO(response.content)
        reader = PdfReader(pdf)
        resume_text = "".join([page.extract_text() or "" for page in reader.pages])
        return resume_text[:15000]
    except:
        return "Resume could not be loaded."

resume_text = load_resume_text()


# -------------------- STREAMLIT UI --------------------
st.set_page_config(page_title="Voice Chat with Nagaphani", page_icon="🎤")
st.title("🎤 Nagaphani’s AI Career Voice Assistant")
st.caption("Ask about experience, AI projects, certifications, or résumé.")

st.divider()

# -------------------- RECRUITER INTRO --------------------
st.markdown("👋 **Hi, I’m Nagaphani’s AI Career Assistant (Voice Mode).**")
st.write("Before we speak, please share the company/role you are recruiting for.")

recruiter_intro = st.text_area("Company / Position Details:", "")

if not recruiter_intro.strip():
    st.info("Please provide recruiter/company details to enable voice input.")
else:
    st.success("Great! You can now record your voice.")


# -------------------- BROWSER AUDIO RECORDER --------------------
st.markdown("### 🎙️ Tap below to record your question:")

audio_bytes = st.audio_input("Record your question")

if audio_bytes and recruiter_intro.strip():

    st.info("🎧 Processing your audio…")

    # -------------------- STEP 1: Audio → Text --------------------
    transcript = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=audio_bytes
    )
    user_text = transcript.text

    st.write("🗣️ **You said:**", user_text)

    # -------------------- CONTACT KEYWORDS --------------------
    keyword_hits = any(k in user_text.lower() for k in [
        "contact", "phone", "email", "linkedin", "resume", "pdf", "qr", "download"
    ])

    if keyword_hits:
        reply_text = (
            f"My contact details are: Phone {PHONE}, Email {EMAIL}, "
            "and my résumé and LinkedIn profile are available on request."
        )
        st.subheader("📞 Contact Information")
        st.markdown(f"""
        **Phone:** {PHONE}  
        **Email:** {EMAIL}  
        **LinkedIn:** https://www.linkedin.com/in/phani2lead/  
        **Résumé:** [View PDF]({RESUME_VIEW_URL})
        """)

        try:
            st.image(QR_IMAGE_PATH, width=180)
        except:
            pass

    else:
        # -------------------- PROFESSIONAL CONTEXT --------------------
        extra_context = """
        Nagaphani Buddepu is currently available for immediate joining.
        He has expertise in AI Delivery, Digital Transformation,
        Product Leadership, Agile/DevOps/MLOps, ISO compliance,
        and enterprise-scale AI modernization.

        Ideal roles: Head of AI Delivery, AI Transformation Leader,
        Chief Digital & AI Officer, Enterprise AI Program Director.
    
        Current CTC ~55 LPA; Expected 80 LPA – 1 Cr for global positions.
        """
    
        # -------------------- CLEAN & NORMALIZE TRANSCRIPT --------------------
        cleaned_text = user_text.lower()
        cleaned_text = cleaned_text.replace("fanny", "phani")
        cleaned_text = cleaned_text.replace("funny", "phani")
        cleaned_text = cleaned_text.replace("pani", "phani")
        cleaned_text = cleaned_text.replace("fani", "phani")
    
        # -------------------- INTENT REWRITE --------------------
        intent_rewrite_prompt = f"""
        Rewrite this recruiter question clearly, fixing name mistakes
        (Fanny -> Nagaphani or Phani), and rewriting it in clean English:
        {cleaned_text}
        """
    
        rewritten = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": intent_rewrite_prompt}]
        )
    
        rewritten_question = rewritten.choices[0].message.content
        st.write("🔍 **Interpreted Question:**", rewritten_question)
    
        # -------------------- ENHANCED SYSTEM PROMPT --------------------
        career_prompt = f"""
        You are an AI Career Assistant representing **Mrs. Nagaphani Buddepu**, a female AI/ML leader and digital transformation professional.
        Use female pronouns (she/her) at all times. Never use he/him.

    
        The recruiter said:
        "{recruiter_intro}"
    
        Use both résumé and professional context to answer clearly
        and confidently. Highlight leadership strengths, AI delivery,
        scaling teams, product vision, and CEO-readiness.
    
        Assume:
        - Any mispronunciation still means Nagaphani.
        - Never say "not in my résumé" unless totally unrelated.
        - If the topic is leadership, growth, CEO role, scaling from 20 to 100,
          ALWAYS give a strong executive-level answer.
    
        Professional Context:
        {extra_context}
    
        Résumé:
        {resume_text}

        Recruiter question (corrected):
        {rewritten_question}
        """
    
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": career_prompt}]
        )
    
        reply_text = completion.choices[0].message.content
        st.write("🤖 **AI Response:**", reply_text)

    # -------------------- STEP 3: Text → Speech --------------------
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=reply_text
    )

    st.success("Generating audio response…")

    st.audio(speech.read(), format="audio/mp3")
