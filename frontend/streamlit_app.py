import streamlit as st
import requests
import os
import numpy as np
import tempfile
import soundfile as sf
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_URL = "http://localhost:8080"

st.set_page_config(page_title="Speaking Coach", layout="wide")
st.title("🎙️ AI Speaking Coach")

# State Initialization
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "current_audio_url" not in st.session_state:
    st.session_state.current_audio_url = None
if "current_user_audio_url" not in st.session_state:
    st.session_state.current_user_audio_url = None
if "transcription" not in st.session_state:
    st.session_state.transcription = ""

# Sidebar
with st.sidebar:
    st.header("Setup")
    topic = st.text_input("Topic", "Life")
    context = st.text_input("Context", "General")
    level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"], index=1)
    
    if st.button("Start New Session"):
        logger.info(f"UI: Starting session for topic='{topic}', context='{context}'")
        resp = requests.post(f"{API_URL}/session/", json={
            "topic": topic,
            "context": context,
            "level": level
        })
        if resp.status_code == 200:
            st.session_state.session_id = resp.json()["id"]
            st.session_state.current_question = None
            st.session_state.transcription = ""
            st.success(f"Session {st.session_state.session_id} Started")
        else:
            st.error("Failed to start session.")

# Tabs
tab_practice, tab_history = st.tabs(["🚀 Practice", "📊 Your History"])

with tab_practice:
    if st.session_state.session_id:
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("Practice Area")
            if st.button("Get Question"):
                with st.spinner("AI is thinking..."):
                    resp = requests.post(f"{API_URL}/question/generate?session_id={st.session_state.session_id}", timeout=600)
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.current_question = data["question"]
                        st.session_state.current_audio_url = data["audio_url"]
                        st.session_state.transcription = "" 
            
            if st.session_state.current_question:
                st.info(st.session_state.current_question)
                if st.session_state.current_audio_url:
                    st.write("🔊 **Listen to Question:**")
                    st.audio(f"{API_URL}{st.session_state.current_audio_url}", format="audio/wav")
                
                st.write("---")
                st.write("### 🎤 Record Your Answer")
                from audio_recorder_streamlit import audio_recorder
                audio_bytes = audio_recorder(text="Speak...", recording_color="#e8b62c", neutral_color="#6aa36f", icon_size="2x")

                if audio_bytes:
                    st.audio(audio_bytes, format="audio/wav")
                    if st.button("Transcribe Answer"):
                        with st.spinner("Transcribing..."):
                            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                                tmp.write(audio_bytes)
                                tmp_path = tmp.name
                            try:
                                with open(tmp_path, "rb") as f:
                                    files = {"file": ("recording.wav", f, "audio/wav")}
                                    resp = requests.post(f"{API_URL}/audio/transcribe?session_id={st.session_state.session_id}", files=files)
                                    if resp.status_code == 200:
                                        data = resp.json()
                                        st.session_state.transcription = data["text"]
                                        st.session_state.current_user_audio_url = data.get("user_audio_url")
                                        logger.info(f"UI: Transcription received: {st.session_state.transcription[:50]}...")
                            finally:
                                if os.path.exists(tmp_path): os.remove(tmp_path)

        with col2:
            st.header("Evaluation")
            if st.session_state.transcription:
                st.success(f"**Transcription:** {st.session_state.transcription}")
                if st.button("Get Feedback"):
                    with st.spinner("Analyzing..."):
                        resp = requests.post(f"{API_URL}/evaluate/", params={
                            "session_id": st.session_state.session_id,
                            "question": st.session_state.current_question,
                            "answer": st.session_state.transcription,
                            "question_audio_url": st.session_state.current_audio_url,
                            "user_audio_url": st.session_state.current_user_audio_url
                        }, timeout=600)
                        if resp.status_code == 200:
                            st.write(resp.json()["feedback"])
            else:
                st.info("Your response and feedback will appear here.")
    else:
        st.info("Please start a session in the sidebar to begin.")

with tab_history:
    st.header("Practice History")
    resp = requests.get(f"{API_URL}/history/")
    if resp.status_code == 200:
        history = resp.json()
        if not history:
            st.write("No practice logs found yet.")
        else:
            for item in history:
                with st.expander(f"📅 {item['date'][:10]} | 🏷️ {item['topic']} ({item['level']})"):
                    st.write(f"**Q:** {item['question']}")
                    if item['question_audio_url']:
                        st.audio(f"{API_URL}{item['question_audio_url']}", format="audio/wav")
                    st.write(f"**Your Answer:** {item['answer']}")
                    if item.get('user_audio_url'):
                        st.audio(f"{API_URL}{item['user_audio_url']}", format="audio/wav")
                    
                    st.markdown("**AI Feedback:**")
                    st.write(item['feedback'])
                    
                    if st.button(f"🗑️ Delete Log {item['id']}", key=f"del_{item['id']}"):
                        del_resp = requests.delete(f"{API_URL}/history/{item['id']}")
                        if del_resp.status_code == 200:
                            st.success("Log deleted!")
                            st.rerun()
                        else:
                            st.error("Failed to delete.")
                    st.write("---")
    else:
        st.error("Could not load history.")
