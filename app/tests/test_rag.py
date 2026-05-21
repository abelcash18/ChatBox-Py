from __future__ import annotations

from pathlib import Path

import pytest

from app.rag import RagEngine


def test_retrieve_returns_results(tmp_path: Path):
    data_dir = tmp_path / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    (data_dir / "doc1.txt").write_text(
        "FastAPI is a modern web framework for building APIs with Python.",
        encoding="utf-8",
    )

    rag = RagEngine(data_dir=data_dir, chunk_size=200, overlap=20)
    results = rag.retrieve("What is FastAPI?", top_k=3)

    assert len(results) > 0
    assert "text" in results[0]
    assert "source" in results[0]
    assert "score" in results[0]

