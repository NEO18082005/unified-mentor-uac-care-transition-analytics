import csv
from datetime import datetime
from pathlib import Path


DATA_PATH = Path(__file__).parents[1] / "data" / "HHS_Unaccompanied_Alien_Children_Program.csv"
EXPECTED_COLUMNS = [
    "Date",
    "Children apprehended and placed in CBP custody*",
    "Children in CBP custody",
    "Children transferred out of CBP custody",
    "Children in HHS Care",
    "Children discharged from HHS Care",
]


def test_source_schema_and_row_count():
    with DATA_PATH.open(newline="", encoding="utf-8-sig") as handle:
        rows = [row for row in csv.DictReader(handle) if row["Date"].strip()]
    assert list(rows[0]) == EXPECTED_COLUMNS
    assert len(rows) == 720


def test_dates_and_values_are_valid():
    with DATA_PATH.open(newline="", encoding="utf-8-sig") as handle:
        rows = [row for row in csv.DictReader(handle) if row["Date"].strip()]
    dates = [datetime.strptime(row["Date"], "%B %d, %Y") for row in rows]
    assert min(dates).date().isoformat() == "2023-01-12"
    assert max(dates).date().isoformat() == "2025-12-21"
    numeric_fields = EXPECTED_COLUMNS[1:]
    for row in rows:
        for field in numeric_fields:
            assert int(row[field].replace(",", "")) >= 0
