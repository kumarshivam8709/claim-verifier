from typing import List
import uuid
import openai
import os

class Claim:
    """Data schema for a claim."""
    def __init__(self, text: str):
        self.id = str(uuid.uuid4())
        self.text = text
        self.entities = []  # Placeholder for entity extraction
        self.time_context = "" # Placeholder for time context

def extract_claims(text: str) -> List[Claim]:
    """Uses an LLM to extract factual claims from the provided text."""
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt = f"""
    You are an expert fact-checker. Your task is to extract clear, verifiable factual claims from the following text.
    Identify claims that can be proven or disproven with external evidence.
    Provide the claims as a Python list of strings. Each string should be a single claim.
    If no claims are found, return an empty list.
    
    Example:
    Text: "The company's new product, the 'FusionX', was released on May 15, 2024. It is the first device to use quantum-powered batteries, which allow it to run for up to 500 hours on a single charge."
    Output: ["The company's new product, the 'FusionX', was released on May 15, 2024.", "The FusionX is the first device to use quantum-powered batteries.", "The FusionX can run for up to 500 hours on a single charge."]
    
    Text: \"\"\"
    {text}
    \"\"\"
    Output:
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        response_text = response.choices[0].message.content.strip()
        
        # A simple way to parse the list from the LLM output.
        # This can be made more robust with Pydantic for schema enforcement.
        import ast
        claims_list = ast.literal_eval(response_text)
        return [Claim(c) for c in claims_list]
    except Exception as e:
        # st.error(f"Error extracting claims: {e}")
        return []