import json
from pathlib import Path

from queryproof.interpreter import interpret_question


def test_evaluation_set_maps_to_expected_intents() -> None:
    cases_path = Path(__file__).resolve().parents[1] / "evals" / "cases.json"
    cases = json.loads(cases_path.read_text(encoding="utf-8"))

    assert len(cases) >= 20
    for case in cases:
        interpretation = interpret_question(case["question"])
        assert interpretation.spec is not None, case["question"]
        assert interpretation.spec.query_id == case["intent"], case["question"]


def test_unknown_question_is_not_forced_into_an_intent() -> None:
    interpretation = interpret_question("Write a poem about databases")

    assert interpretation.spec is None
    assert interpretation.confidence == 0.0
