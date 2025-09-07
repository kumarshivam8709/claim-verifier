import streamlit as st
import io_utils
import claims
import search_retrieval
import stance
import scoring
import explain
import ui_components
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set Streamlit page configuration
st.set_page_config(
    page_title="AI-Powered Misinformation Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "claims" not in st.session_state:
    st.session_state.claims = []
if "evidence" not in st.session_state:
    st.session_state.evidence = {}
if "judgments" not in st.session_state:
    st.session_state.judgments = {}
if "assessments" not in st.session_state:
    st.session_state.assessments = {}

def main():
    """Main Streamlit app function."""
    st.title("AI-Powered Misinformation Assistant")
    st.markdown("A tool to help identify and verify claims, packaged as a shareable credibility card. ")

    with st.sidebar:
        st.header("Settings")
        mode = st.radio(
            "Select Input Mode:",
            ("URL", "Text", "Screenshot"),
        )
        domain = st.selectbox(
            "Select Domain Focus:",
            ("General", "Health", "Elections", "Finance"),
        )
        st.checkbox("Privacy Mode (Redact PII)", value=False)
        st.markdown("---")
        st.subheader("Project Modules")
        st.write("Each module handles a specific part of the verification pipeline.")

    st.markdown("---")

    st.header("Analyze a Claim")
    input_text = ""
    input_file = None

    if mode == "URL":
        input_text = st.text_input("Enter a URL:")
    elif mode == "Text":
        input_text = st.text_area("Paste text here:")
    elif mode == "Screenshot":
        input_file = st.file_uploader("Upload a screenshot (PNG/JPG):", type=["png", "jpg", "jpeg"])

    if st.button("Analyze"):
        with st.spinner("Processing..."):
            # Step 1: Claim extraction
            st.markdown("### Step 1: Extracting Claims")
            raw_text = ""
            if input_text:
                if mode == "URL":
                    raw_text = io_utils.fetch_url_content(input_text)
                else:
                    raw_text = input_text
            elif input_file:
                raw_text = io_utils.extract_text_from_image(input_file.read())
            
            st.session_state.claims = claims.extract_claims(raw_text)
            st.success(f"Found {len(st.session_state.claims)} claims.")

            if st.session_state.claims:
                # Step 2 & 3: Retrieval and Stance
                st.markdown("### Step 2 & 3: Retrieving Evidence & Assessing Stance")
                for c in st.session_state.claims:
                    st.write(f"Analyzing claim: **{c.text}**")
                    st.session_state.evidence[c.id] = search_retrieval.search_for_evidence(c.text)
                    st.session_state.judgments[c.id] = stance.classify_stance(c.text, st.session_state.evidence[c.id])
                    st.session_state.assessments[c.id] = scoring.score_risk(c, st.session_state.judgments[c.id])

                st.success("Analysis complete!")

    st.markdown("---")

    st.header("Results")
    if st.session_state.claims:
        for c in st.session_state.claims:
            with st.container(border=True):
                ui_components.render_result_card(c, st.session_state.judgments.get(c.id, []), st.session_state.assessments.get(c.id))
        
        st.download_button(
            label="Download Credibility Card",
            data=explain.generate_credibility_card(st.session_state.claims, st.session_state.judgments, st.session_state.assessments),
            file_name="credibility_card.pdf",
            mime="application/pdf",
        )

        st.markdown("---")
        st.header("How to Verify")
        st.markdown(explain.get_micro_lesson("lateral_reading"))
        st.markdown("---")
        st.header("Evaluation")
        st.write("This is a placeholder for a built-in evaluation page.")
    else:
        st.info("Start by entering a URL, text, or screenshot to analyze.")
    
    st.markdown("---")
    st.markdown("#### Limitations")
    st.markdown("This tool is for educational purposes and should not be used as a sole source of truth. Results are based on available public data and AI model interpretation, which can be limited.")


if __name__ == "__main__":
    main()