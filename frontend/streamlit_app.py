import streamlit as st
import requests
import os
import numpy as np
import tempfile
import soundfile as sf
import logging
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase

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
        resp = requests.post(f"{API_URL}/session/", json={"topic": topic, "context": context})
        if resp.status_code == 200:
            st.session_state.session_id = resp.json()["id"]
            st.session_state.current_question = None
            st.session_state.transcription = ""
            st.success("Session Started")

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.audio_frames = []

    def recv(self, frame):
        self.audio_frames.append(frame.to_ndarray())
        return frame

# UI
if st.session_state.session_id:
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Practice")
        if st.button("Get Question"):
            with st.spinner("AI is thinking (CPU inference, please wait)..."):
                resp = requests.post(
                    f"{API_URL}/question/generate?session_id={st.session_state.session_id}",
                    timeout=300
                )
                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state.current_question = data["question"]
                    st.session_state.current_audio_url = data["audio_url"]
                    st.session_state.transcription = "" # Reset transcription for new question
        
        if st.session_state.current_question:
            st.info(st.session_state.current_question)
            
            # Persistent Audio Player
            if st.session_state.current_audio_url:
                st.write("🔊 **Listen to Question:**")
                st.audio(f"{API_URL}{st.session_state.current_audio_url}", format="audio/wav", autoplay=True)
            
            st.write("---")
            st.write("### 🎤 Record Your Answer")
            webrtc_ctx = webrtc_streamer(
                key="speech",
                mode=WebRtcMode.SENDONLY,
                audio_processor_factory=AudioProcessor,
                media_stream_constraints={"video": False, "audio": True},
                rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
            )

            if webrtc_ctx.audio_processor:
                if st.button("Finish & Transcribe"):
                    frames = webrtc_ctx.audio_processor.audio_frames
                    if frames:
                        with st.spinner("Transcribing..."):
                            audio_data = np.concatenate(frames, axis=0)
                            if len(audio_data.shape) > 1:
                                audio_data = audio_data.mean(axis=1)
                            
                            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                                sf.write(tmp.name, audio_data, 48000)
                                with open(tmp.name, "rb") as f:
                                    files = {"file": ("recording.wav", f, "audio/wav")}
                                    resp = requests.post(f"{API_URL}/audio/transcribe?session_id={st.session_state.session_id}", files=files)
                                    if resp.status_code == 200:
                                        st.session_state.transcription = resp.json()["text"]
                        os.remove(tmp.name)
                    else:
                        st.warning("No audio captured.")

    with col2:
        st.header("Transcription")
        if st.session_state.transcription:
            st.success(st.session_state.transcription)
            if st.button("Get Feedback"):
                with st.spinner("AI Evaluating..."):
                    resp = requests.post(f"{API_URL}/evaluate/", params={
                        "session_id": st.session_state.session_id,
                        "question": st.session_state.current_question,
                        "answer": st.session_state.transcription
                    })
                    if resp.status_code == 200:
                        st.markdown("### Feedback")
                        st.write(resp.json()["feedback"])
        else:
            st.info("Your transcription will appear here.")
else:
    st.info("Start a session.")
