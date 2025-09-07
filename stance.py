from typing import List
from claims import Claim
from search_retrieval import Evidence
import openai
import os

class StanceJudgment:
    """Data schema for stance classification."""
    def __init__(self, claim_id: str, evidence_url: str, label: str, confidence: float, quote_span: str):
        self.claim_id = claim_id
        self.evidence_url = evidence_url
        self.label = label
        self.confidence = confidence
        self.quote_span = quote_span

def classify_stance(claim_text: str, evidence_list: List[Evidence]) -> List[StanceJudgment]:
    """Classifies the stance of each evidence snippet relative to a claim."""
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    judgments = []

    for evidence in evidence_list:
        prompt = f"""
        You are an expert fact-checker. Your task is to determine the stance of the provided EVIDENCE relative to the CLAIM.
        The stance can be one of three labels: SUPPORT, REFUTE, or NEI (Not Enough Info).
        You must also extract a direct quote from the EVIDENCE that best supports your stance.
        
        CLAIM: "{claim_text}"
        
        EVIDENCE (Snippet from {evidence.domain}): "{evidence.snippet}"
        
        Based on the evidence snippet, what is the stance?
        Provide a JSON object with the following keys:
        - "label": The stance label (SUPPORT, REFUTE, or NEI).
        - "confidence": A confidence score (0.0 to 1.0).
        - "quote_span": The exact quote from the EVIDENCE snippet that justifies your label.
        
        Example Output:
        ```json
        {{
            "label": "SUPPORT",
            "confidence": 0.95,
            "quote_span": "The device can run for up to 500 hours on a single charge"
        }}
        ```
        
        Output:
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            import json
            judgment_data = json.loads(response.choices[0].message.content)
            
            judgments.append(
                StanceJudgment(
                    claim_id="", # Placeholder, will be filled in the main app
                    evidence_url=evidence.url,
                    label=judgment_data.get("label", "NEI"),
                    confidence=judgment_data.get("confidence", 0.0),
                    quote_span=judgment_data.get("quote_span", "")
                )
            )
        except Exception as e:
            print(f"Error classifying stance for evidence {evidence.url}: {e}")
            judgments.append(
                StanceJudgment(
                    claim_id="",
                    evidence_url=evidence.url,
                    label="NEI",
                    confidence=0.0,
                    quote_span="Error processing this evidence."
                )
            )
            
    return judgments