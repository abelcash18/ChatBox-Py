from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


def test_root_returns_html():
    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    assert "text/html" in r.headers.get("content-type", "")


def test_chat_endpoint_returns_reply(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    # Patch rag engine data_dir to an isolated temp folder
    from app import main as main_mod

    data_dir = tmp_path / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "doc.txt").write_text("Python lets you build reliable systems.", encoding="utf-8")

    # Replace rag
    main_mod.rag = main_mod.RagEngine(data_dir=data_dir)

    client = TestClient(main_mod.app)
    resp = client.post("/api/chat", json={"message": "What is Python for?"})
    assert resp.status_code == 200

    body = resp.json()
    assert "reply" in body
    assert isinstance(body["reply"], str)
    assert "retrieved" in body

