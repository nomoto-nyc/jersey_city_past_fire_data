"""Download Jersey City incident and unit-count data from NERIS Public."""

import csv
import json
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parent
URL = (
    "https://lpbcyjocolyzmvo6.svcs5.arcgis.com/lPbcyJOcoLyZmvo6/ArcGIS/rest/"
    "services/NERIS%20Public%20Incident%20Basics/FeatureServer/0/query"
)
DEPT_ID = "FD34017554"
FIELDS = [
    "ObjectId", "neris_id_incident", "neris_id_dept", "department_name",
    "call_create", "type_1", "type_1_primary", "unit_response_count",
    "duration", "aid_direction", "incident_county", "incident_state",
    "export_date",
    # Location
    "x", "y", "civic_location", "type_location_use", "type_location_use__second",
    "in_use", "intended", "type_vacancy",
    # Additional incident types and context
    "type_2", "type_3", "special_modifiers", "nonfd_aid", "rescue_animal",
    "department_state", "action_and_tactics",
    # Fire outcome
    "room_of_origin", "point_origin", "building_damage", "acres_burned",
    "exposure_count", "displacement_count", "displacement_causes",
    # Detection and suppression
    "smoke_alarm_present", "smoke_alarm_types", "smoke_alarm_operation",
    "fire_suppression_present", "fire_suppression_types", "fire_suppression_operation",
    # Hazard flags
    "csst_hazard_flag", "electric_hazard_flag", "powergen_hazard_flag",
    "medical_oxygen_hazard_flag",
]


def query(**params):
    args = {"where": f"neris_id_dept = '{DEPT_ID}'", "f": "json", **params}
    url = URL + "?" + urllib.parse.urlencode(args)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=75) as response:
                data = json.load(response)
            if "error" in data:
                raise RuntimeError(data["error"])
            return data
        except (TimeoutError, OSError):
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)


def date_of(value, tz):
    if value is None:
        return ""
    return datetime.fromtimestamp(value / 1000, timezone.utc).astimezone(tz).isoformat()


def main():
    count = query(returnCountOnly="true")["count"]
    rows = []
    for offset in range(0, count, 1000):
        data = query(
            outFields=",".join(FIELDS), returnGeometry="false",
            resultOffset=str(offset), resultRecordCount="1000",
            orderByFields="ObjectId ASC",
        )
        batch = [feature["attributes"] for feature in data["features"]]
        if not batch:
            raise RuntimeError(f"Empty page at offset {offset}")
        rows.extend(batch)
        print(f"Fetched {len(rows)}/{count}", flush=True)
    if len(rows) != count or len({row["ObjectId"] for row in rows}) != count:
        raise RuntimeError("Record count or ObjectId uniqueness check failed")

    eastern = ZoneInfo("America/New_York")
    out = ROOT / "neris_jersey_city_incidents.csv"
    with out.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS + ["call_create_eastern", "export_date_eastern"])
        writer.writeheader()
        for row in rows:
            writer.writerow({**row,
                "call_create_eastern": date_of(row["call_create"], eastern),
                "export_date_eastern": date_of(row["export_date"], eastern)})

    by_type = defaultdict(lambda: {"incidents": 0, "known_unit_responses": 0, "missing_unit_counts": 0})
    by_month = defaultdict(lambda: {"incidents": 0, "known_unit_responses": 0, "missing_unit_counts": 0})
    counts = Counter()
    for row in rows:
        category = (row["type_1"] or "UNKNOWN").split("||")[0]
        month = date_of(row["call_create"], eastern)[:7] or "UNKNOWN"
        units = row["unit_response_count"]
        for bucket in (by_type[category], by_month[month]):
            bucket["incidents"] += 1
            if units is None:
                bucket["missing_unit_counts"] += 1
            else:
                bucket["known_unit_responses"] += units
        counts[str(units)] += 1
    summary = {
        "source": URL.rsplit("/query", 1)[0],
        "department_id": DEPT_ID,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "incident_count": count,
        "earliest_call_eastern": min(date_of(r["call_create"], eastern) for r in rows if r["call_create"]),
        "latest_call_eastern": max(date_of(r["call_create"], eastern) for r in rows if r["call_create"]),
        "by_type": dict(sorted(by_type.items())),
        "by_month": dict(sorted(by_month.items())),
        "unit_count_distribution": dict(sorted(counts.items(), key=lambda x: (x[0] == "None", float(x[0]) if x[0] != "None" else 0))),
    }
    (ROOT / "neris_jersey_city_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
