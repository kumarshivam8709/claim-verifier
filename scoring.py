from typing import List
from claims import Claim
from stance import StanceJudgment

class RiskAssessment:
    """Data schema for a risk assessment."""
    def __init__(self, claim_id: str, risk: str, score: float, rationale: str):
        self.claim_id = claim_id
        self.risk = risk
        self.score = score
        self.rationale = rationale

def score_risk(claim: Claim, judgments: List[StanceJudgment]) -> RiskAssessment:
    """Calculates a risk score for a claim based on stance judgments."""
    support_count = sum(1 for j in judgments if j.label == "SUPPORT")
    refute_count = sum(1 for j in judgments if j.label == "REFUTE")
    nei_count = sum(1 for j in judgments if j.label == "NEI")

    total_judgments = len(judgments)
    
    # Simple scoring logic based on the project plan
    if refute_count > support_count:
        risk_score = (refute_count / total_judgments) * 0.8 + 0.2 # Higher base for refuting evidence
        risk = "HIGH"
        rationale = "Multiple sources refute this claim."
    elif nei_count / total_judgments > 0.5:
        risk_score = 0.5
        risk = "MED"
        rationale = "Lack of independent corroboration or sufficient evidence."
    elif support_count > 0:
        risk_score = 1.0 - (support_count / total_judgments) * 0.7 # Lower score for supporting evidence
        if support_count / total_judgments > 0.8:
            risk = "LOW"
            rationale = "Multiple sources independently support this claim."
        else:
            risk = "MED"
            rationale = "Some supporting evidence found, but not consistently corroborated."
    else:
        risk_score = 0.75 # Default to medium if no clear evidence
        risk = "MED"
        rationale = "No clear evidence found to support or refute the claim."

    # Clamp the score to be between 0 and 1
    risk_score = max(0.0, min(1.0, risk_score))
    
    return RiskAssessment(
        claim_id=claim.id,
        risk=risk,
        score=risk_score,
        rationale=rationale
    )