import hashlib
from functools import lru_cache
from pathlib import Path
from typing import Any

import duckdb

from .catalog import QuerySpec
from .interpreter import interpret_question
from .models import AnalysisResponse, ChartPoint, Evidence, TraceStep

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "support_tickets.csv"
SOURCE_LABEL = "data/support_tickets.csv"


@lru_cache(maxsize=1)
def dataset_sha256() -> str:
    return hashlib.sha256(DATA_PATH.read_bytes()).hexdigest()


@lru_cache(maxsize=1)
def row_count() -> int:
    with DATA_PATH.open("rb") as handle:
        return max(0, sum(1 for _ in handle) - 1)


def dataset_metadata() -> dict[str, Any]:
    return {
        "source": SOURCE_LABEL,
        "rows": row_count(),
        "sha256": dataset_sha256(),
        "synthetic": True,
        "seed": 42,
    }


def _connection() -> duckdb.DuckDBPyConnection:
    connection = duckdb.connect(database=":memory:", config={"threads": "1"})
    safe_path = DATA_PATH.as_posix().replace("'", "''")
    connection.execute(
        f"CREATE TABLE tickets AS SELECT * FROM read_csv_auto('{safe_path}', header = true)"
    )
    return connection


def _run(spec: QuerySpec) -> list[ChartPoint]:
    with _connection() as connection:
        cursor = connection.execute(spec.sql)
        rows = cursor.fetchall()

    return [
        ChartPoint(
            label=str(row[0]),
            value=float(row[1]),
            secondary=float(row[2]) if row[2] is not None else None,
        )
        for row in rows[:50]
    ]


def _answer(spec: QuerySpec, chart: list[ChartPoint]) -> tuple[str, str]:
    top = chart[0]
    if spec.query_id == "ticket_volume_by_queue":
        return (
            f"{top.label} is the busiest queue with {int(top.value)} tickets.",
            f"It represents {top.secondary:.1f}% of the synthetic dataset.",
        )
    if spec.query_id == "csat_weekly_trend":
        start, end = chart[0], chart[-1]
        direction = "increased" if end.value >= start.value else "decreased"
        return (
            f"Weekly CSAT {direction} from {start.value:.2f} to {end.value:.2f}.",
            "Only submitted survey scores are included; missing CSAT remains missing, not zero.",
        )
    if spec.query_id == "first_contact_resolution_by_queue":
        return (
            f"{top.label} leads first-contact resolution at {top.value:.1f}%.",
            f"The rate is calculated across {int(top.secondary or 0)} synthetic tickets.",
        )
    if spec.query_id == "escalation_rate_by_category":
        return (
            f"{top.label} has the highest escalation rate at {top.value:.1f}%.",
            "Categories with fewer than 20 tickets are excluded to avoid unstable rankings.",
        )
    if spec.query_id == "resolution_time_by_queue":
        return (
            f"{top.label} has the longest average resolution time at {top.value:.1f} minutes.",
            "The metric uses resolved duration for every ticket in the queue.",
        )
    return (
        f"{top.label} is the largest contact channel at {top.value:.1f}%.",
        f"That corresponds to {int(top.secondary or 0)} synthetic tickets.",
    )


def analyze_question(question: str) -> AnalysisResponse:
    interpretation = interpret_question(question)
    metadata = dataset_metadata()

    if interpretation.spec is None:
        return AnalysisResponse(
            supported=False,
            intent="unsupported",
            answer="This deterministic demo cannot map that question to an approved analysis.",
            explanation=(
                "Choose one of the example questions or ask about volume, CSAT, FCR, "
                "escalations, resolution time or channel mix."
            ),
            chart_title="No query executed",
            unit="count",
            chart=[],
            sql="-- No SQL executed: the question did not match the allowlist.",
            evidence=Evidence(
                source=SOURCE_LABEL,
                dataset_sha256=metadata["sha256"],
                rows_scanned=0,
                rows_returned=0,
                query_id="none",
            ),
            trace=[
                TraceStep(
                    label="Classify intent",
                    detail="No approved intent passed the confidence threshold.",
                    status="blocked",
                )
            ],
        )

    spec = interpretation.spec
    chart = _run(spec)
    answer, explanation = _answer(spec, chart)
    match_detail = interpretation.matched_phrase or "weighted keyword evidence"

    return AnalysisResponse(
        supported=True,
        intent=spec.query_id,
        answer=answer,
        explanation=explanation,
        chart_title=spec.chart_title,
        unit=spec.unit,
        chart=chart,
        sql=spec.sql,
        evidence=Evidence(
            source=SOURCE_LABEL,
            dataset_sha256=metadata["sha256"],
            rows_scanned=metadata["rows"],
            rows_returned=len(chart),
            query_id=spec.query_id,
        ),
        trace=[
            TraceStep(
                label="Classify intent",
                detail=(
                    f"Matched {spec.query_id} using {match_detail}; "
                    f"confidence {interpretation.confidence:.0%}."
                ),
            ),
            TraceStep(
                label="Inspect source",
                detail=f"Loaded {metadata['rows']} rows from a seeded synthetic CSV.",
            ),
            TraceStep(
                label="Execute allowlisted SQL",
                detail="Ran a read-only catalog query in an isolated in-memory DuckDB connection.",
            ),
            TraceStep(
                label="Attach evidence",
                detail=(
                    "Returned the SQL, source hash, row counts and chart values with the answer."
                ),
            ),
        ],
    )
