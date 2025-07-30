import streamlit as st
import requests

st.set_page_config(page_title="RA Copilot MVP", layout="wide")

st.title("🧠 RA Copilot – MVP Demo")

st.sidebar.header("Session Controls")
session_name = st.sidebar.text_input("Session Name", placeholder="e.g. MDR Gap Review")
uploaded_file = st.sidebar.file_uploader("Upload transcript", type=["txt", "md", "vtt"])

st.markdown("### Paste Transcript or Meeting Notes")
transcript = st.text_area("Transcript Input", height=300, placeholder="Paste your transcript here...")

if st.button("Analyze"):
    if not transcript.strip():
        st.error("Please paste some transcript or notes first.")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/analyze",
                json={"transcript": transcript},
                timeout=10
            )
            response.raise_for_status()
            result = response.json().get("result", "No result returned.")
            st.success(result)
        except Exception as e:
            st.error(f"❌ Analysis failed: {e}")

st.markdown("---")
st.markdown("ℹ️ This MVP demo will later show guidance cards based on regulatory frameworks like MDR, ISO 13485, and FDA 21 CFR 820.")
