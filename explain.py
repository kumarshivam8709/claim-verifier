from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Flowable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from typing import List
from claims import Claim
from stance import StanceJudgment
from scoring import RiskAssessment
import datetime
import io

# Dummy data for lessons
LESSONS = {
    "lateral_reading": """
        **Lateral Reading Micro-Lesson** 🕵️‍♀️
        
        Instead of reading "down" a single article, read "laterally."
        
        1.  **Open multiple sources:** When you encounter a new claim, open several new tabs to see what other reputable sources say about it.
        2.  **Check the source:** Who is the author? What is the domain? Is it a well-known news organization, a blog, or a known misinformation site?
        3.  **Find the consensus:** Look for what the majority of reliable sources are saying. If a claim is only supported by a few unknown sites, it's likely unreliable.
        """,
    "sift": "SIFT is a framework for fact-checking...",
    # Add other lessons as needed
}

class Line(Flowable):
    def __init__(self, width=1*inch, color=(0, 0, 0)):
        Flowable.__init__(self)
        self.width = width
        self.strokeColor = color

    def draw(self):
        self.canv.line(0, self.height, self.width, self.height)

def get_micro_lesson(topic: str) -> str:
    """Returns the text for a micro-lesson."""
    return LESSONS.get(topic, "No lesson found for this topic.")

def generate_credibility_card(
    claims: List[Claim],
    judgments: dict,
    assessments: dict
) -> bytes:
    """Generates a PDF credibility card with a summary of the analysis."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Title
    title_style = styles["h1"]
    title_style.alignment = TA_CENTER
    story.append(Paragraph("Credibility Card", title_style))
    story.append(Spacer(1, 0.2 * inch))
    
    # Timestamp
    story.append(Paragraph(f"Last Verified: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Line(doc.width))
    story.append(Spacer(1, 0.2 * inch))

    for claim in claims:
        assessment = assessments.get(claim.id)
        claim_judgments = judgments.get(claim.id, [])
        
        story.append(Paragraph(f"**Claim:** {claim.text}", styles["h2"]))
        if assessment:
            story.append(Paragraph(f"**Risk Level:** {assessment.risk} (Score: {assessment.score:.2f})", styles["Normal"]))
            story.append(Paragraph(f"**Rationale:** {assessment.rationale}", styles["Normal"]))

        story.append(Spacer(1, 0.1 * inch))
        story.append(Paragraph("Top Sources:", styles["h3"]))
        
        # Group judgments by label
        support_sources = [j for j in claim_judgments if j.label == "SUPPORT"]
        refute_sources = [j for j in claim_judgments if j.label == "REFUTE"]

        if support_sources:
            story.append(Paragraph("- Supporting:", styles["Normal"]))
            for j in support_sources[:3]: # List top 3
                story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp; - <a href='{j.evidence_url}'>{j.evidence_url}</a>", styles["Normal"]))
                story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;Quote: \"{j.quote_span}\"", styles["Italic"]))
        
        if refute_sources:
            story.append(Paragraph("- Refuting:", styles["Normal"]))
            for j in refute_sources[:3]: # List top 3
                story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp; - <a href='{j.evidence_url}'>{j.evidence_url}</a>", styles["Normal"]))
                story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;Quote: \"{j.quote_span}\"", styles["Italic"]))

        story.append(Spacer(1, 0.2 * inch))
        story.append(Line(doc.width))
        story.append(Spacer(1, 0.2 * inch))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()