import os
from typing import List
# from serpapi import SerpApiSearch # Import the correct class
from serpapi import GoogleSearch

class Evidence:
    """Data schema for a piece of evidence."""
    def __init__(self, url: str, domain: str, published_date: str, snippet: str):
        self.url = url
        self.domain = domain
        self.published_date = published_date
        self.snippet = snippet

def search_for_evidence(claim_text: str) -> List[Evidence]:
    """Uses SERPAPI to find relevant web pages for a claim."""
    api_key = os.environ.get("SERPAPI_API_KEY")
    if not api_key:
        return [Evidence(url="#", domain="Error", published_date="", snippet="SERPAPI_API_KEY not set.")]
    
    params = {
        "q": claim_text,
        "api_key": api_key,
        "engine": "google",
        "num": 10,
    }

    try:
        # Create an instance of the class
        # search = SerpApiSearch(params=params)
        search = GoogleSearch(params)
        # Call the get_dict method on the instance
        search_results = search.get_dict()
        
        evidence_list = []
        
        for result in search_results.get("organic_results", []):
            evidence_list.append(
                Evidence(
                    url=result.get("link", "#"),
                    domain=result.get("source", "N/A"),
                    published_date=result.get("date", "N/A"),
                    snippet=result.get("snippet", "No snippet available.")
                )
            )
        return evidence_list
    except Exception as e:
        return [Evidence(url="#", domain="Error", published_date="", snippet=f"Search API Error: {e}")]