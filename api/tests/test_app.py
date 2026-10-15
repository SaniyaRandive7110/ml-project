import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


def test_health():
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_predict():
    client = app.test_client()
    res = client.post("/predict", json={"features": [5.1, 3.5, 1.4, 0.2]})
    assert res.status_code == 200
    assert "prediction" in res.get_json()


def test_predict_bad_input():
    client = app.test_client()
    res = client.post("/predict", json={"features": "abc"})
    assert res.status_code == 400
