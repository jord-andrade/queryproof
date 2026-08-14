import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response

from queryproof import analyze_question, dataset_metadata
from queryproof.models import AnalysisRequest, AnalysisResponse

app = FastAPI(
    title="QueryProof API",
    description="Deterministic, traceable analytics over a synthetic dataset.",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)


@app.middleware("http")
async def response_metadata(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    started = time.perf_counter()
    request_id = request.headers.get("x-request-id", str(uuid.uuid4()))[:64]
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    response.headers["x-process-time-ms"] = f"{(time.perf_counter() - started) * 1000:.1f}"
    response.headers["x-content-type-options"] = "nosniff"
    return response


@app.exception_handler(Exception)
async def unhandled_error(_request: Request, _error: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": "The analysis could not be completed."},
    )


@app.get("/api")
def api_index() -> dict[str, object]:
    return {
        "name": "QueryProof API",
        "version": "1.0.0",
        "mode": "deterministic",
        "documentation": "/api/docs",
        "health": "/api/health",
    }


@app.get("/api/health")
def health() -> dict[str, object]:
    return {"status": "ok", "mode": "deterministic", "dataset": dataset_metadata()}


@app.get("/api/schema")
def schema() -> dict[str, object]:
    return {
        "table": "tickets",
        "synthetic": True,
        "columns": [
            {"name": "ticket_id", "type": "VARCHAR"},
            {"name": "created_at", "type": "DATE"},
            {"name": "week", "type": "VARCHAR"},
            {"name": "queue", "type": "VARCHAR"},
            {"name": "category", "type": "VARCHAR"},
            {"name": "channel", "type": "VARCHAR"},
            {"name": "resolution_minutes", "type": "INTEGER"},
            {"name": "first_contact_resolution", "type": "INTEGER"},
            {"name": "csat", "type": "DOUBLE", "nullable": True},
            {"name": "escalated", "type": "INTEGER"},
        ],
    }


@app.get("/api/examples")
def examples() -> dict[str, list[str]]:
    return {
        "questions": [
            "Which queue receives the most tickets?",
            "How has CSAT changed week over week?",
            "What is first-contact resolution by queue?",
            "Which category has the highest escalation rate?",
            "Which queue takes the longest to resolve?",
            "How are contacts split by channel?",
        ]
    }


@app.post("/api/analyze", response_model=AnalysisResponse)
def analyze(payload: AnalysisRequest) -> AnalysisResponse:
    return analyze_question(payload.question)
