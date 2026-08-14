import csv
import math
import random
from datetime import date, timedelta
from pathlib import Path
from typing import TypedDict

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "support_tickets.csv"
SEED = 42
ROWS = 960


class QueueSettings(TypedDict):
    categories: tuple[str, ...]
    minutes: int
    fcr: float
    csat: float
    escalation: float


QUEUES: dict[str, QueueSettings] = {
    "Account": {
        "categories": ("Sign-in", "Profile settings", "Subscription change"),
        "minutes": 19,
        "fcr": 0.84,
        "csat": 4.48,
        "escalation": 0.07,
    },
    "Playback": {
        "categories": ("Buffering", "Video quality", "Audio and subtitles"),
        "minutes": 28,
        "fcr": 0.75,
        "csat": 4.18,
        "escalation": 0.13,
    },
    "Billing": {
        "categories": ("Payment failed", "Refund request", "Invoice question"),
        "minutes": 37,
        "fcr": 0.67,
        "csat": 3.96,
        "escalation": 0.20,
    },
    "Devices": {
        "categories": ("Device activation", "Compatibility", "Device limit"),
        "minutes": 31,
        "fcr": 0.72,
        "csat": 4.08,
        "escalation": 0.16,
    },
}


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def generate_rows() -> list[dict[str, object]]:
    randomizer = random.Random(SEED)
    start = date(2026, 1, 5)
    queue_names = tuple(QUEUES)
    queue_weights = (0.25, 0.34, 0.22, 0.19)
    rows: list[dict[str, object]] = []

    for index in range(ROWS):
        created_at = start + timedelta(days=randomizer.randrange(84))
        week_index = (created_at - start).days // 7
        queue = randomizer.choices(queue_names, weights=queue_weights, k=1)[0]
        settings = QUEUES[queue]
        category = randomizer.choice(settings["categories"])
        channel = randomizer.choices(("Chat", "Email", "Phone"), (0.56, 0.29, 0.15), k=1)[0]

        improvement = week_index * 0.004
        first_contact = randomizer.random() < clamp(settings["fcr"] + improvement, 0.0, 0.95)
        escalated = randomizer.random() < clamp(
            settings["escalation"] - improvement / 2,
            0.03,
            0.45,
        )
        channel_multiplier = {"Chat": 0.86, "Email": 1.18, "Phone": 1.05}[channel]
        resolution = round(
            max(
                4,
                randomizer.gauss(settings["minutes"] * channel_multiplier, 7.5)
                * (1.2 if escalated else 1.0),
            )
        )

        if randomizer.random() < 0.13:
            csat: object = ""
        else:
            csat_value = settings["csat"] + week_index * 0.015
            csat_value -= 0.42 if escalated else 0
            csat_value += 0.12 if first_contact else -0.08
            csat = round(clamp(randomizer.gauss(csat_value, 0.38), 1.0, 5.0), 1)

        iso_year, iso_week, _ = created_at.isocalendar()
        rows.append(
            {
                "ticket_id": f"TKT-{index + 1:04d}",
                "created_at": created_at.isoformat(),
                "week": f"{iso_year}-W{iso_week:02d}",
                "queue": queue,
                "category": category,
                "channel": channel,
                "resolution_minutes": resolution,
                "first_contact_resolution": int(first_contact),
                "csat": csat,
                "escalated": int(escalated),
            }
        )

    return rows


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rows = generate_rows()
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(rows[0]),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    size_kb = math.ceil(OUTPUT.stat().st_size / 1024)
    print(f"generated {len(rows)} synthetic rows at {OUTPUT} ({size_kb} KB)")


if __name__ == "__main__":
    main()
