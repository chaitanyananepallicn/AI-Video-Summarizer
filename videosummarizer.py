import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import upload_file, get_file
import google.generativeai as genai

from translator import translate_text
from text_to_speech import text_to_audio_autoplay

import time
from pathlib import Path
import tempfile
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    st.error("GOOGLE_API_KEY not found in .env")

st.set_page_config(page_title="Gemini Video Summarizer", layout="wide")

st.markdown("""
<style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        background-color: #0a0a0a;
        color: #e0e0e0;
    }
    .main .block-container {
        max-width: 960px;
        padding-top: 1rem;
        margin: auto;
    }
    video {
        width: 100%;
        max-width: 720px;
        height: 240px;
        border-radius: 12px;
        margin: 0 auto;
        display: block;
        box-shadow: 0 4px 12px rgba(255,255,255,0.1);
    }
    .stButton>button {
        width: 100%;
        background-color: #333333;
        color: #f5f5f5;
        font-size: 16px;
        padding: 10px;
        border-radius: 8px;
    }
    .stSelectbox, .stTextArea, .stFileUploader {
        margin-bottom: 20px;
    }
    .summary-box {
        background-color: #1c1c1c;
        border-radius: 10px;
        padding: 15px;
        color: #e0e0e0;
        box-shadow: 0 2px 6px rgba(255,255,255,0.1);
    }
    .summary-columns {
        display: flex;
        gap: 20px;
    }
    .summary-columns > div {
        flex: 1;
    }
</style>
""", unsafe_allow_html=True)

st.title("Gemini Video AI Summarizer")
st.markdown("""
#### Translate | Text-to-Speech | Gemini-Powered Insights
Upload a video and ask anything about its content. Summaries are auto-translated and spoken aloud in your language.
""")

@st.cache_resource
def initialize_agent():
    return Agent(
        name="Video AI Summarizer",
        model=Gemini(id="gemini-2.0-flash"),
        tools=[DuckDuckGo()],
        markdown=True,
    )

agent = initialize_agent()

video_file = st.file_uploader("Upload a Video", type=["mp4", "mov", "avi"])
target_lang = st.selectbox("Select Output Language", ["English", "Telugu", "Hindi", "French", "Spanish"])

if video_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(video_file.read())
        video_path = temp_video.name

    st.video(video_path)
    user_query = st.text_area("Ask a question about the video:", height=100)

    if st.button("Analyze & Translate"):
        if not user_query.strip():
            st.warning("Please enter your query.")
        else:
            try:
                with st.spinner("Processing with Gemini..."):
                    processed_video = upload_file(video_path)
                    while processed_video.state.name == "PROCESSING":
                        time.sleep(1)
                        processed_video = get_file(processed_video.name)

                    prompt = f"""
You are an expert content analyzer.

Analyze the uploaded video and generate a comprehensive essay-style response that includes:
- A suitable **Title** for the video content.
- The **Subject** or theme the video discusses.
- A detailed explanation of **every major topic or point** covered in the video.
- Break the explanation into clear **sections or paragraphs**.
- Use **subheadings** if needed for clarity.
- Make sure the essay is structured, informative, and written in a **human-friendly tone**.

User Query: {user_query}
"""
                    response = agent.run(prompt, videos=[processed_video])
                    st.session_state.english_summary = response.content.strip()

                    if target_lang != "English":
                        st.session_state.translated = translate_text(
                            st.session_state.english_summary, target_lang
                        )

            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                Path(video_path).unlink(missing_ok=True)

# Display summaries and audio
if "english_summary" in st.session_state:
    st.subheader("Summary")
    st.markdown("<div class='summary-columns'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**English Summary**")
        st.markdown(f"<div class='summary-box'>{st.session_state.english_summary}</div>", unsafe_allow_html=True)
        if st.button("Play English Summary"):
            file_path, _ = text_to_audio_autoplay(st.session_state.english_summary, lang="en", return_path=True)
            if Path(file_path).exists():
                st.audio(file_path, format="audio/mp3", start_time=0)
                st.info("Click play to listen.")

    with col2:
        if "translated" in st.session_state and target_lang != "English":
            st.markdown(f"**Translated Summary ({target_lang})**")
            st.markdown(f"<div class='summary-box'>{st.session_state.translated}</div>", unsafe_allow_html=True)
            lang_map = {
                "English": "en", "Telugu": "te", "Hindi": "hi", "French": "fr", "Spanish": "es"
            }
            if st.button(f"Play {target_lang} Summary"):
                file_path, _ = text_to_audio_autoplay(
                    st.session_state.translated, lang=lang_map.get(target_lang, "en"), return_path=True
                )
                if Path(file_path).exists():
                    st.audio(file_path, format="audio/mp3", start_time=0)
                    st.info("Click play to listen.")

    st.markdown("</div>", unsafe_allow_html=True)