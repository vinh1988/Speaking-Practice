import streamlit as st
import requests
import os
import numpy as np
import tempfile
import soundfile as sf
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_URL = "http://localhost:8080"

st.set_page_config(page_title="Speaking Coach", layout="wide")
st.title("🎙️ AI Speaking Coach")

# State
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "current_audio_url" not in st.session_state:
    st.session_state.current_audio_url = None
if "transcription" not in st.session_state:
    st.session_state.transcription = ""

# Sidebar
with st.sidebar:
    st.header("Setup")
    topic = st.text_input("Topic", "Life")
    context = st.text_input("Context", "General")
    if st.button("Start Session"):
        logger.info(f"UI: Starting session for topic='{topic}', context='{context}'")
        resp = requests.post(f"{API_URL}/session/", json={"topic": topic, "context": context})
        logger.info(f"Backend: Session creation response status: {resp.status_code}")
        if resp.status_code == 200:
            st.session_state.session_id = resp.json()["id"]
            logger.info(f"UI: Session started with ID: {st.session_state.session_id}")
            st.session_state.current_question = None
            st.session_state.transcription = ""
            st.success("Session Started")
        else:
            logger.error(f"Backend Error: {resp.text}")



# UI
if st.session_state.session_id:
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Practice")
        if st.button("Get Question"):
            logger.info(f"UI: Requesting question for session {st.session_state.session_id}")
            with st.spinner("AI is thinking (CPU inference, please wait)..."):
                resp = requests.post(
                    f"{API_URL}/question/generate?session_id={st.session_state.session_id}",
                    timeout=300
                )
                logger.info(f"Backend: Question generation response status: {resp.status_code}")
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state.current_question = data["question"]
                    st.session_state.current_audio_url = data["audio_url"]
                    logger.info(f"UI: Received question: {st.session_state.current_question[:50]}...")
                    st.session_state.transcription = "" # Reset transcription for new question
                else:
                    logger.error(f"Backend Error: {resp.text}")
        
        if st.session_state.current_question:
            st.info(st.session_state.current_question)
            
            # Persistent Audio Player
            if st.session_state.current_audio_url:
                st.write("🔊 **Listen to Question:**")
                st.audio(f"{API_URL}{st.session_state.current_audio_url}", format="audio/wav", autoplay=True)
            
            st.write("---")
            st.write("### 🎤 Record Your Answer")
            from audio_recorder_streamlit import audio_recorder
            
            audio_bytes = audio_recorder(
                text="Click to record your answer (click again to stop)",
                recording_color="#e8b62c",
                neutral_color="#6aa36f",
                icon_size="2x",
                pause_threshold=60.0, # Increased to avoid early stop during thinking pauses
                key="audio_recorder_comp"
            )

            if audio_bytes:
                st.audio(audio_bytes, format="audio/wav")
                if st.button("Transcribe Answer"):
                    logger.info(f"UI: Starting transcription for captured audio ({len(audio_bytes)} bytes)")
                    with st.spinner("Transcribing..."):
                        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                            tmp.write(audio_bytes)
                            tmp_path = tmp.name
                        
                        try:
                            with open(tmp_path, "rb") as f:
                                files = {"file": ("recording.wav", f, "audio/wav")}
                                resp = requests.post(f"{API_URL}/audio/transcribe?session_id={st.session_state.session_id}", files=files)
                                logger.info(f"Backend: Transcription response status: {resp.status_code}")
                                if resp.status_code == 200:
                                    st.session_state.transcription = resp.json()["text"]
                                    logger.info(f"UI: Transcription received: {st.session_state.transcription[:50]}...")
                                else:
                                    logger.error(f"Backend Error: {resp.text}")
                                    st.error(f"Transcription failed: {resp.text}")
                        finally:
                            if os.path.exists(tmp_path):
                                os.remove(tmp_path)
            else:
                st.info("Click the microphone icon and speak. It will stop automatically or when you click again.")

    with col2:
        st.header("Transcription")
        if st.session_state.transcription:
            st.success(st.session_state.transcription)
            if st.button("Get Feedback"):
                logger.info("UI: Requesting evaluation for current answer")
                with st.spinner("AI Evaluating..."):
                    resp = requests.post(f"{API_URL}/evaluate/", params={
                        "session_id": st.session_state.session_id,
                        "question": st.session_state.current_question,
                        "answer": st.session_state.transcription
                    })
                    logger.info(f"Backend: Evaluation response status: {resp.status_code}")
                    if resp.status_code == 200:
                        st.markdown("### Feedback")
                        feedback = resp.json()["feedback"]
                        st.write(feedback)
                        logger.info(f"UI: Received feedback: {feedback[:50]}...")
                    else:
                        logger.error(f"Backend Error: {resp.text}")
        else:
            st.info("Your transcription will appear here.")
else:
    st.info("Start a session.")
