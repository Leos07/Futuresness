from fastapi.testclient import TestClient
from api.main import app
import json

client = TestClient(app)


def test_analyze_endpoint_basic():
    text = "Scenario planning and horizon scanning are common foresight methods. Backcasting may also appear."
    resp = client.post('/analyze', data={'text': text, 'cooccurrence_window': '100'})
    assert resp.status_code == 200
    data = resp.json()
    assert 'statistics' in data
    assert 'word_frequencies' in data
    assert 'co_occurrences' in data
    assert 'csv' in data
    assert 'clusters' in data


def test_analyze_endpoint_large_text_rejected():
    # generate very large text
    big = 'word ' * 300000  # ~1.2M chars
    resp = client.post('/analyze', data={'text': big})
    assert resp.status_code == 413 or resp.status_code == 400