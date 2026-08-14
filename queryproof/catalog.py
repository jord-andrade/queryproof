from dataclasses import dataclass
from typing import Literal

Unit = Literal["count", "percent", "minutes", "score"]


@dataclass(frozen=True)
class QuerySpec:
    query_id: str
    chart_title: str
    unit: Unit
    keywords: tuple[str, ...]
    sql: str


QUERY_SPECS: tuple[QuerySpec, ...] = (
    QuerySpec(
        query_id="ticket_volume_by_queue",
        chart_title="Ticket volume by queue",
        unit="count",
        keywords=("most tickets", "ticket volume", "busiest queue", "tickets by queue"),
        sql="""SELECT
  queue AS label,
  COUNT(*)::INTEGER AS value,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS secondary
FROM tickets
GROUP BY queue
ORDER BY value DESC, label ASC""",
    ),
    QuerySpec(
        query_id="csat_weekly_trend",
        chart_title="Weekly customer satisfaction",
        unit="score",
        keywords=("csat", "customer satisfaction", "satisfaction trend", "satisfaction score"),
        sql="""SELECT
  week AS label,
  ROUND(AVG(csat), 2) AS value,
  COUNT(csat)::INTEGER AS secondary
FROM tickets
WHERE csat IS NOT NULL
GROUP BY week
ORDER BY week ASC""",
    ),
    QuerySpec(
        query_id="first_contact_resolution_by_queue",
        chart_title="First-contact resolution by queue",
        unit="percent",
        keywords=("first contact", "fcr", "resolved on first", "first-contact"),
        sql="""SELECT
  queue AS label,
  ROUND(100.0 * AVG(first_contact_resolution), 1) AS value,
  COUNT(*)::INTEGER AS secondary
FROM tickets
GROUP BY queue
ORDER BY value DESC, label ASC""",
    ),
    QuerySpec(
        query_id="escalation_rate_by_category",
        chart_title="Escalation rate by category",
        unit="percent",
        keywords=("escalation", "escalated", "highest escalation", "escalation rate"),
        sql="""SELECT
  category AS label,
  ROUND(100.0 * AVG(escalated), 1) AS value,
  COUNT(*)::INTEGER AS secondary
FROM tickets
GROUP BY category
HAVING COUNT(*) >= 20
ORDER BY value DESC, label ASC
LIMIT 8""",
    ),
    QuerySpec(
        query_id="resolution_time_by_queue",
        chart_title="Average resolution time by queue",
        unit="minutes",
        keywords=("resolution time", "longest to resolve", "slowest queue", "average minutes"),
        sql="""SELECT
  queue AS label,
  ROUND(AVG(resolution_minutes), 1) AS value,
  COUNT(*)::INTEGER AS secondary
FROM tickets
GROUP BY queue
ORDER BY value DESC, label ASC""",
    ),
    QuerySpec(
        query_id="channel_mix",
        chart_title="Contact channel mix",
        unit="percent",
        keywords=("channel mix", "split by channel", "contact channel", "chat email phone"),
        sql="""SELECT
  channel AS label,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS value,
  COUNT(*)::INTEGER AS secondary
FROM tickets
GROUP BY channel
ORDER BY value DESC, label ASC""",
    ),
)


SPECS_BY_ID = {spec.query_id: spec for spec in QUERY_SPECS}
