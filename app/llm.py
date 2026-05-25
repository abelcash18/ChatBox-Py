from __future__ import annotations

import os
from typing import List, Dict


def generate_reply(*, user_message: str, retrieved_chunks: List[Dict[str, str]]) -> str:
    """Generate a reply using either:
    - OpenAI (if OPENAI_API_KEY is set)
    - Local mock (default)

    To keep this project runnable anywhere, the default is a deterministic mock.
    """

    api_key = os.getenv("OPENAI_API_KEY")
    print(f"DEBUG: OPENAI_API_KEY is set: {bool(api_key)}")  # Debug line
    if api_key:
        # Optional OpenAI integration. Kept minimal to avoid forcing a dependency.
        try:
            from openai import OpenAI  # type: ignore

            client = OpenAI(api_key=api_key)
            context = "\n\n".join(
                f"Source: {c.get('source')} (chunk {c.get('chunk_id')})\n{c.get('text')}" for c in retrieved_chunks
            )
            prompt = (
                "You are a helpful assistant. Use the provided context to answer.\n"
                "If the context is insufficient, say so and answer generally.\n\n"
                f"CONTEXT:\n{context}\n\n"
                f"USER: {user_message}\nASSISTANT:"
            )

            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            # Fall back to mock if anything fails
            print(f"DEBUG: OpenAI API error: {type(e).__name__}: {str(e)}")
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

