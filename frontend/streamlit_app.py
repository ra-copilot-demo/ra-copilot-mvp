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
        # Placeholder for analysis results
        st.info("Analyzing your transcript…")
        # TODO: Call backend /analyze endpoint
        st.success("✅ Placeholder: Analysis complete!")
