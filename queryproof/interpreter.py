import re
from dataclasses import dataclass

from .catalog import QUERY_SPECS, QuerySpec


@dataclass(frozen=True)
class Interpretation:
    spec: QuerySpec | None
    confidence: float
    matched_phrase: str | None


TOKEN_HINTS: dict[str, tuple[str, ...]] = {
    "ticket_volume_by_queue": ("volume", "tickets", "queue", "busiest", "most"),
    "csat_weekly_trend": ("csat", "satisfaction", "weekly", "trend", "score"),
    "first_contact_resolution_by_queue": ("fcr", "first", "contact", "resolve", "queue"),
    "escalation_rate_by_category": ("escalation", "escalated", "category", "rate", "highest"),
    "resolution_time_by_queue": ("resolution", "time", "minutes", "slowest", "longest"),
    "channel_mix": ("channel", "mix", "chat", "email", "phone", "split"),
}


def normalize_question(question: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9\s-]", " ", question.lower()).split())


def interpret_question(question: str) -> Interpretation:
    normalized = normalize_question(question)
    tokens = set(normalized.replace("-", " ").split())
    ranked: list[tuple[float, QuerySpec, str | None]] = []

    for spec in QUERY_SPECS:
        phrase_matches = [phrase for phrase in spec.keywords if phrase in normalized]
        token_matches = tokens.intersection(TOKEN_HINTS[spec.query_id])
        score = len(phrase_matches) * 4.0 + len(token_matches) * 0.8
        ranked.append((score, spec, phrase_matches[0] if phrase_matches else None))

    score, spec, matched_phrase = max(ranked, key=lambda item: item[0])
    if score < 2.4:
        return Interpretation(spec=None, confidence=0.0, matched_phrase=None)

    confidence = min(0.99, round(0.62 + score / 20, 2))
    return Interpretation(spec=spec, confidence=confidence, matched_phrase=matched_phrase)
