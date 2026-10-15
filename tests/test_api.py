from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_caption_requires_a_file():
    assert client.post("/caption").status_code == 422
