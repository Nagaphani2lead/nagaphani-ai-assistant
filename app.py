import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import requests
from io import BytesIO

# -------------------- CONFIG --------------------
client = OpenAI(api_key="OPENAI_API_KEY")   # 👈 Replace with your OpenAI API key

# Resume link (Google Drive direct link)
RESUME_VIEW_URL = "https://drive.google.com/file/d/1A9fGkLL-oP9LbPNWLsWjevBzHb5Qx3Ki/view?usp=sharing"
RESUME_DOWNLOAD_URL = "https://drive.google.com/uc?id=1A9fGkLL-oP9LbPNWLsWjevBzHb5Qx3Ki"

# Contact details
PHONE = "+91-7304060673"
EMAIL = "nagaphani.leads@gmail.com"
QR_IMAGE_PATH = "Nagaphani_Buddepu_QR_Stylish.png"

# -------------------- LOAD RESUME TEXT --------------------
try:
    response = requests.get(RESUME_DOWNLOAD_URL)
    pdf = BytesIO(response.content)
    reader = PdfReader(pdf)
    resume_text = "".join([page.extract_text() or "" for page in reader.pages])
except Exception as e:
    resume_text = "Resume could not be loaded."
    st.error(f"Error reading resume: {e}")

# -------------------- UI --------------------
st.set_page_config(page_title="Chat with Nagaphani", page_icon="🤖")
st.title("💬 Chat with Nagaphani's AI Career Assistant")
st.caption("Ask about my experience, certifications, AI projects, or request my résumé/contact details.")

question = st.text_input("Type your question here...")

# -------------------- RESPONSE LOGIC --------------------
if question.strip():
    q = question.lower()
    keywords = ["contact", "phone", "email", "resume", "pdf", "qr", "connect", "download"]

    if any(k in q for k in keywords):
        st.subheader("📞 Contact Information")
        st.markdown(f"""
        - **Phone:** {PHONE}  
        - **Email:** [{EMAIL}](mailto:{EMAIL})  
        - **Résumé:** [View PDF]({RESUME_VIEW_URL})
        """)
        try:
            st.image(QR_IMAGE_PATH, caption="📄 Scan to view my résumé", width=180)
        except:
            st.warning("QR image not found in this environment.")
        st.download_button(
            label="📥 Download Résumé (PDF)",
            data=response.content if 'response' in locals() else b'',
            file_name="Nagaphani_Buddepu_Resume.pdf",
            mime="application/pdf",
        )
    else:
        prompt = f"""
        You are an AI assistant for Nagaphani Buddepu.
        Use the following resume content to answer clearly and professionally.
        Resume:
        {resume_text}

        Question: {question}
        """
        try:
            reply = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
            )
            st.success(reply.choices[0].message.content)
        except Exception as e:
            st.error(f"AI error: {e}")
else:
    st.info("👆 Type a question above to chat with your AI profile assistant.")

st.markdown("---")
st.caption("🤖 Designed by Nagaphani Buddepu | AI Delivery • Product Leadership • Transformation Excellence")
