from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Chunk:
    text: str
    source: str
    chunk_id: int


class RagEngine:
    """A tiny local RAG engine.

    - Loads .txt files from `data/`
    - Splits into chunks (by characters with overlap)
    - Builds TF-IDF embeddings for all chunks
    - Retrieves top-k similar chunks via cosine similarity
    """

    def __init__(self, data_dir: Path, *, chunk_size: int = 1200, overlap: int = 200):
        self.data_dir = Path(data_dir)
        self.chunk_size = chunk_size
        self.overlap = overlap

        self.chunks: List[Chunk] = []
        self.vectorizer: TfidfVectorizer | None = None
        self.chunk_matrix: np.ndarray | None = None

        self._build_index()

    def _iter_docs(self):
        if not self.data_dir.exists():
            return
        for p in sorted(self.data_dir.glob("**/*.txt")):
            yield p

    def _chunk_text(self, text: str) -> List[str]:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = "\n".join(line.strip() for line in text.splitlines() if line.strip())

        chunks = []
        i = 0
        while i < len(text):
            end = min(len(text), i + self.chunk_size)
            chunks.append(text[i:end])
            if end == len(text):
                break
            i = max(0, end - self.overlap)
        return chunks

    def _build_index(self) -> None:
        self.chunks = []

        chunk_texts: List[str] = []
        for doc in self._iter_docs():
            raw = doc.read_text(encoding="utf-8", errors="ignore")
            for idx, c in enumerate(self._chunk_text(raw)):
                chunk = Chunk(text=c, source=str(doc.relative_to(self.data_dir)), chunk_id=idx)
                self.chunks.append(chunk)
                chunk_texts.append(c)

        if not chunk_texts:
            # Fallback so the app always works
            fallback = "No documents found in data/. Add .txt files to enable retrieval."
            self.chunks = [Chunk(text=fallback, source="(fallback)", chunk_id=0)]
            chunk_texts = [fallback]

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=6000,
            ngram_range=(1, 2),
        )
        self.chunk_matrix = self.vectorizer.fit_transform(chunk_texts)

    def retrieve(self, query: str, *, top_k: int = 4) -> List[Dict[str, str]]:
        if not query.strip():
            return []
        assert self.vectorizer is not None and self.chunk_matrix is not None

        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.chunk_matrix).flatten()
        top_indices = np.argsort(-sims)[:top_k]

        results: List[Dict[str, str]] = []
        for i in top_indices:
            c = self.chunks[int(i)]
            score = float(sims[int(i)])
            results.append({
                "text": c.text[:500] + ("..." if len(c.text) > 500 else ""),
                "source": c.source,
                "chunk_id": str(c.chunk_id),
                "score": f"{score:.4f}",
            })
        return results

