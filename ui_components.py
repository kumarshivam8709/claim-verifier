import streamlit as st
from claims import Claim
from stance import StanceJudgment
from scoring import RiskAssessment
from typing import List

def render_result_card(claim: Claim, judgments: List[StanceJudgment], assessment: RiskAssessment):
    """Renders a single result card for a claim."""
    st.subheader(f"Claim: {claim.text}")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("##### **Risk Assessment**")
        if assessment:
            if assessment.risk == "LOW":
                st.markdown(f":green[**{assessment.risk}**]")
                st.progress(assessment.score, text=f"Score: {assessment.score:.2f}")
            elif assessment.risk == "MED":
                st.markdown(f":orange[**{assessment.risk}**]")
                st.progress(assessment.score, text=f"Score: {assessment.score:.2f}")
            else:
                st.markdown(f":red[**{assessment.risk}**]")
                st.progress(assessment.score, text=f"Score: {assessment.score:.2f}")
            st.info(f"Rationale: {assessment.rationale}")
        else:
            st.warning("Assessment not available.")

    with col2:
        st.markdown("##### **Evidence Tiles**")
        if judgments:
            for j in judgments:
                with st.expander(f"{j.label} from {j.evidence_url}"):
                    st.markdown(f"**Confidence:** {j.confidence:.2f}")
                    st.markdown(f"**Quote:** \"{j.quote_span}\"")
        else:
            st.info("No evidence found for this claim.")