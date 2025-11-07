# Chatbot
streamlit
openai
PyPDF2
requests
# Voicebot
pip install openai streamlit sounddevice numpy scipy

# Architecture
#🎙️ Microphone input (speech → text)
#     ↓
#🔧 OpenAI Chat Completion (your existing prompt)
#     ↓
#🗣️ OpenAI Text-to-Speech (or other TTS)
#     ↓
#🔁 Play audio back in Streamlit

