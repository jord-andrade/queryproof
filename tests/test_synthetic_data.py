import csv
import re
from pathlib import Path


def test_public_dataset_has_no_identity_columns_or_contact_values() -> None:
    data_path = Path(__file__).resolve().parents[1] / "data" / "support_tickets.csv"
    with data_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    assert len(rows) == 960
    assert not {"name", "email", "phone", "agent_name", "supervisor"}.intersection(
        {column.lower() for column in reader.fieldnames or []}
    )

    text_fields = ("ticket_id", "queue", "category", "channel")
    public_text = "\n".join(",".join(row[field] for field in text_fields) for row in rows)
    assert re.search(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", public_text) is None
    assert re.search(r"\+?\d[\d\s().-]{8,}\d", public_text) is None
