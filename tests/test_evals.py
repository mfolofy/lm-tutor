"""Tests for the eval history logger and profile command."""

import json
import tempfile
from pathlib import Path

import pytest

from tutor.eval import grade
from tutor.registrar.evals import EvalHistory


@pytest.fixture
def history():
    """Create an EvalHistory with a temp directory."""
    with tempfile.TemporaryDirectory() as tmp:
        yield EvalHistory(state_dir=Path(tmp))


def test_record_and_load(history):
    """Recording an eval result and loading it returns the same data."""
    result = grade('<img src="x.png">', "brushes")
    history.record("test-model", result)
    records = history.load("test-model")
    assert len(records) == 1
    assert records[0]["model"] == "test-model"
    assert records[0]["passed"] is False
    assert records[0]["violation_count"] >= 1


def test_multiple_records(history):
    """Multiple eval records are appended, not overwritten."""
    history.record("test-model", grade("<div>pass</div>", "brushes"))
    history.record("test-model", grade('<img src="x.png">', "brushes"))
    records = history.load("test-model")
    assert len(records) == 2


def test_per_model_isolation(history):
    """Records for different models are isolated."""
    history.record("model-a", grade("<div>ok</div>", "brushes"))
    history.record("model-b", grade('<img src="x.png">', "brushes"))
    assert len(history.load("model-a")) == 1
    assert len(history.load("model-b")) == 1


def test_per_class_pass_rates(history):
    """Pass rates aggregate correctly."""
    # Two passes, one fail for brushes
    history.record("test-model", grade("<html lang='en'>ok</html>", "brushes"))
    history.record("test-model", grade("<html lang='en'>ok</html>", "brushes"))
    history.record("test-model", grade('<img src="x.png">', "brushes"))

    rates = history.per_class_pass_rates("test-model")
    assert "brushes" in rates
    assert rates["brushes"]["attempts"] == 3
    assert rates["brushes"]["passes"] == 2
    assert rates["brushes"]["pass_rate"] == pytest.approx(0.667, rel=0.01)


def test_weakest_rules(history):
    """Weakest rules are sorted by failure count."""
    # One img-alt violation, two button-name
    history.record("test-model", grade('<img src="x.png"><button></button>', "brushes"))
    history.record("test-model", grade("<button></button>", "brushes"))

    weak = history.weakest_rules("test-model", top_n=5)
    # button-name appears twice, img-alt once
    assert len(weak) >= 2
    btn = next(w for w in weak if w["rule"] == "button-name")
    img = next(w for w in weak if w["rule"] == "img-alt")
    assert btn["failures"] > img["failures"]


def test_empty_history(history):
    """Loading history for a model with no records returns empty."""
    assert history.load("nonexistent") == []


def test_total_evals(history):
    """total_evals returns correct count."""
    assert history.total_evals("test-model") == 0
    history.record("test-model", grade("<div>ok</div>", "brushes"))
    assert history.total_evals("test-model") == 1


def test_clean_eval_is_recorded(history):
    """A passing eval is recorded correctly."""
    result = grade("<html lang='en'><title>OK</title><body><p>fine</p></body></html>", "brushes")
    assert result.passed
    history.record("test-model", result)
    records = history.load("test-model")
    assert len(records) == 1
    assert records[0]["passed"] is True
    assert records[0]["violation_count"] == 0


def test_jsonl_format(history):
    """The history file is valid JSONL (one JSON object per line)."""
    history.record("test-model", grade("<div>ok</div>", "brushes"))
    history.record("test-model", grade("<div>ok</div>", "brushes"))

    path = history._path_for("test-model")
    lines = path.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 2
    for line in lines:
        assert json.loads(line)  # Valid JSON
        assert "timestamp" in json.loads(line)
