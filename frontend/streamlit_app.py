import streamlit as st
import requests
import os

API_URL = "http://localhost:8080"

st.set_page_config(page_title="AI Speaking Coach", layout="wide")

st.title("🎙️ Multimodal AI Speaking Coach")
st.markdown("---")

# Sidebar for Setup
with st.sidebar:
    st.header("Session Setup")
    topic = st.text_input("Topic", "Traveling")
    context = st.text_input("Context", "IELTS Speaking Part 2")
    level = st.selectbox("Level", ["Beginner", "Intermediate", "Advanced"])
    
    if st.button("Start New Session"):
        resp = requests.post(f"{API_URL}/session/", json={
            "topic": topic,
            "context": context,
            "level": level
        })
        if resp.status_code == 200:
            st.session_state.session_id = resp.json()["id"]
            st.success(f"Session {st.session_state.session_id} started!")

# Main Area
if "session_id" in st.session_state:
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Practice")
        img_file = st.file_uploader("Upload an Image (Optional)", type=["jpg", "png", "jpeg"])
        if img_file:
            st.image(img_file, caption="Uploaded Image", use_column_width=True)
            if st.button("Generate Question from Image"):
                files = {"file": img_file.getvalue()}
                resp = requests.post(f"{API_URL}/image/describe?session_id={st.session_state.session_id}", files={"file": (img_file.name, img_file, img_file.type)})
                if resp.status_code == 200:
                    st.write(f"**AI Vision:** {resp.json()['description']}")
        
        audio_file = st.file_uploader("Upload Your Speaking (WAV)", type=["wav"])
        if audio_file:
            if st.button("Send Answer"):
                files = {"file": (audio_file.name, audio_file, audio_file.type)}
                resp = requests.post(f"{API_URL}/audio/transcribe?session_id={st.session_state.session_id}", files=files)
                if resp.status_code == 200:
                    st.session_state.transcription = resp.json()["text"]
                    st.info(f"**You said:** {st.session_state.transcription}")

    with col2:
        st.header("Feedback")
        if "transcription" in st.session_state:
            st.write("Generating scores...")
            # Here you would call an evaluation endpoint
            st.metric("Grammar", "7.0")
            st.metric("Fluency", "6.5")
            st.info("**Tip:** Try to use more complex sentence structures.")
else:
    st.info("Please start a session in the sidebar to begin.")
