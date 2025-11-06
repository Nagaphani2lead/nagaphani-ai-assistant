import streamlit as st
from openai import OpenAI
from PyPDF2 import PdfReader
import requests
from io import BytesIO
import os

# -------------------- SETUP --------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


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
    resume_text = resume_text[:15000]  # keep only first 15K characters
except Exception as e:
    resume_text = "Resume could not be loaded."
    resume_text = resume_text[:15000]  # keep only first 15K characters

    st.error(f"Error reading resume: {e}")

# -------------------- PAGE HEADER --------------------
st.set_page_config(page_title="Chat with Nagaphani", page_icon="🤖")
st.markdown("## 💬 Chat with Nagaphani's AI Career Assistant")
st.divider()
st.caption("Ask about my experience, certifications, AI projects, or request my résumé/contact details.")

# -------------------- RECRUITER INTRO --------------------
st.markdown("👋 **Hi, I’m Nagaphani’s AI Career Assistant.**")
st.write("Before we chat, could you please tell me a bit about the position or company you’re hiring for?")

recruiter_intro = st.text_area("Can I know more about the position and company, please?", "")

if recruiter_intro:
    st.success("Thank you for sharing that! Let’s continue our conversation.")
else:
    st.info("👆 Please tell me a bit about the position or company before we chat.")

# -------------------- MAIN CHAT --------------------
question = st.text_input("Type your question here...")

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
        # -------------------- PROFESSIONAL CONTEXT --------------------
        extra_context = """
        Nagaphani Buddepu is currently available for immediate joining.

        He brings over a decade of experience in AI delivery, digital transformation, and product leadership.
        He has served as an Agile Transformation Coach, mentoring enterprise teams and startups to scale efficiently
        through modern practices like Agile, DevOps, MLOps, and data-driven innovation.

        Nagaphani is POSH certified, ISO 9001 / 13485 / 27001 compliant documentation expert, and experienced with
        CMMI Level 3 development processes. He has mentored multiple organizations in building quality systems,
        process automation frameworks, and compliance-ready engineering documentation.

        He is open to opportunities across any global location.  
        For positions outside India, he would require a valid work permit.

        When Fortune 500 companies approach him, he is best suited for senior AI Leadership roles such as
        **Head of AI Delivery, AI Transformation Leader, or Enterprise AI Program Director**.  
        When engaging with startups, his vision is to grow as **Chief Digital & AI Officer or Head of Technology**, 
        driving innovation, culture, and digital product maturity from zero to scale.

        He continues to mentor early-stage founders and student innovators in Agile adoption,
        AI modernization, and ethical technology leadership.

        💰 **Compensation Information:**  
        Current package – approximately ₹55 lakhs per annum.  
        Expected range – ₹80 lakhs – ₹1 crore, flexible depending on global role scope and responsibilities.

        For additional professional insights, certifications, and published highlights,
        please visit his LinkedIn profile:  
        https://www.linkedin.com/in/phani2lead/
        """

        prompt = f"""
        You are an AI Career Assistant representing Nagaphani Buddepu.
        This conversation is with a recruiter who shared this about the role:
        "{recruiter_intro}"

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
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
            )
            st.write(response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"⚠️ OpenAI API error: {e}")
    
# -------------------- FOOTER --------------------
if recruiter_intro:
    st.caption(f"✅ Recruiter info noted: {recruiter_intro[:60]}...")
st.markdown("---")
st.caption("🤖 Designed by Nagaphani Buddepu | AI Delivery • Product Leadership • Transformation Excellence")
