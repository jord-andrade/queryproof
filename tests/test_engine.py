from queryproof.engine import analyze_question, dataset_metadata


def test_supported_analysis_carries_reproducible_evidence() -> None:
    result = analyze_question("Which queue receives the most tickets?")
    metadata = dataset_metadata()

    assert result.supported is True
    assert result.intent == "ticket_volume_by_queue"
    assert result.chart
    assert result.evidence.rows_scanned == 960
    assert result.evidence.dataset_sha256 == metadata["sha256"]
    assert result.sql.lstrip().startswith("SELECT")
    assert all(step.status == "complete" for step in result.trace)


def test_unsupported_analysis_executes_no_sql() -> None:
    result = analyze_question("Forecast next year's revenue")

    assert result.supported is False
    assert result.chart == []
    assert result.evidence.rows_scanned == 0
    assert "No SQL executed" in result.sql
