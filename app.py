import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import requests
from io import BytesIO
import os

# Read key from Streamlit Secrets (or local environment)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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
    keywords = ["contact", "linkedin", "phone", "email", "resume", "pdf", "qr", "connect", "download"]

    if any(k in q for k in keywords):
        st.subheader("📞 Contact Information")
        st.markdown(f"""
        - **Phone:** {PHONE}  
        - **Email:** [{EMAIL}](mailto:{EMAIL})  
        - **LinkedIn:** [https://www.linkedin.com/in/phani2lead/](https://www.linkedin.com/in/phani2lead/)  
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
        # -------------------- SMART PROFESSIONAL CONTEXT --------------------
        extra_context = """
        Nagaphani Buddepu is currently available for immediate joining.
        
        He brings over a decade of experience in AI delivery, digital transformation, and product leadership.
        He has served as an Agile Transformation Coach, mentoring enterprise teams and startups to scale efficiently
        through modern practices like Agile, DevOps, MLOps, and data-driven innovation.
        
        Nagaphani is POSH certified, ISO 9001 / 13485 / 27001 compliant documentation expert, and experienced with
        CMMI Level 3 development processes. He has mentored multiple organizations in building quality systems,
        process automation frameworks, and compliance-ready engineering documentation.
        
        She is open to opportunities across any global location.  
        For positions outside India, he would require a valid work permit.
        
        When Fortune 500 companies approach him, he is best suited for senior AI Leadership roles such as
        **Head of AI Delivery, AI Transformation Leader, or Enterprise AI Program Director**.  
        When engaging with startups, his vision is to grow as **Chief Digital & AI Officer or Head of Technology**, 
        driving innovation, culture, and digital product maturity from zero to scale.
        
        He continues to mentor early-stage founders and student innovators in Agile adoption,
        AI modernization, and ethical technology leadership.
        
        For additional professional insights, certifications, and published highlights,
        please visit his LinkedIn profile:  
        https://www.linkedin.com/in/phani2lead/
        """
        prompt = f"""
        You are an AI Career Assistant representing Nagaphani Buddepu.
        Use both the résumé and the professional context below to answer questions clearly, confidently,
        and in a recruiter-friendly tone. Be concise but highlight leadership, transformation, and quality credentials.
        
        If a question isn’t covered in the résumé or context, respond gracefully with:
        "That topic isn't mentioned in my résumé, but I'd be happy to discuss it further."
        
        Professional Context:
        {extra_context}
        
        Résumé:
        {resume_text}
        
        User question: {question}
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
        )
        
        st.write(response.choices[0].message.content)
else:
    st.info("👆 Type a question above to chat with your AI profile assistant.")

st.markdown("---")
st.caption("🤖 Designed by Nagaphani Buddepu | AI Delivery • Product Leadership • Transformation Excellence")
