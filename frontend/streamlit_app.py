import streamlit as st

st.set_page_config(page_title="RA Copilot MVP", page_icon="🤖")

st.title("RA Copilot MVP")
st.write("📋 Paste your meeting transcript or notes below and click Analyze.")

transcript = st.text_area(
    "Meeting Transcript",
    placeholder="Paste transcript text here...",
    height=200
)

if st.button("Analyze"):
    if not transcript.strip():
        st.error("Please paste some transcript or notes first.")
    else:
        st.info("Analyzing your transcript…")
        try:
            import requests
            response = requests.post(
                "http://127.0.0.1:8000/analyze",
                json={"transcript": transcript},
                timeout=10
            )
            response.raise_for_status()
            result = response.json().get("result", "No result returned")
            st.success(result)
        except Exception as e:
            st.error(f"Analysis failed: {e}")