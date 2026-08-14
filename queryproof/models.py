from typing import Literal

from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    question: str = Field(min_length=6, max_length=300)


class ChartPoint(BaseModel):
    label: str
    value: float
    secondary: float | None = None


class Evidence(BaseModel):
    source: str
    dataset_sha256: str
    rows_scanned: int
    rows_returned: int
    query_id: str


class TraceStep(BaseModel):
    label: str
    detail: str
    status: Literal["complete", "blocked"] = "complete"


class AnalysisResponse(BaseModel):
    supported: bool
    intent: str
    answer: str
    explanation: str
    chart_title: str
    unit: Literal["count", "percent", "minutes", "score"]
    chart: list[ChartPoint]
    sql: str
    evidence: Evidence
    trace: list[TraceStep]
