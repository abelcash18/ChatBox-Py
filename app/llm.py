from __future__ import annotations

import os
import requests
from typing import List, Dict


def generate_reply(*, user_message: str, retrieved_chunks: List[Dict[str, str]]) -> str:
    """Generate a reply using either:
    - Serper API for web search (if SERPER_API_KEY is set)
    - Local mock (default)

    To keep this project runnable anywhere, the default is a deterministic mock.
    """

    api_key = os.getenv("SERPER_API_KEY")
    print(f"DEBUG: SERPER_API_KEY is set: {bool(api_key)}")  # Debug line
    if api_key:
        # Optional Serper API integration for web search
        try:
            url = "https://google.serper.dev/search"
            payload = {
                "q": user_message,
                "num": 5
            }
            headers = {
                "X-API-KEY": api_key,
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            results = response.json()
            
            # Extract search results
            search_results = results.get("organic", [])
            if search_results:
                answer = results.get("answer", "")
                if answer:
                    return f"(Serper) {answer}"
                
                # Format top results
                formatted = "(Serper) Based on web search:\n\n"
                for i, result in enumerate(search_results[:3], 1):
                    title = result.get("title", "")
                    snippet = result.get("snippet", "")
                    formatted += f"{i}. {title}\n   {snippet}\n\n"
                return formatted.strip()
            else:
                return "(Serper) No search results found."
        except Exception as e:
            # Fall back to mock if anything fails
            print(f"DEBUG: Serper API error: {type(e).__name__}: {str(e)}")
            pass

    # Mock response: concise and grounded in retrieved chunks
    if retrieved_chunks:
        sources = ", ".join({c.get("source", "?") for c in retrieved_chunks})
        top = retrieved_chunks[0].get("text", "")
        return (
            f"(Mock) I found relevant info in: {sources}.\n\n"
            f"Here’s what it says about your question: \n{top}\n\n"
            f"If you want, ask a more specific question and I’ll try again."
        )

    return "(Mock) I don’t have any retrieved context yet, but I can still help. What do you need?"

