"""Assign every NERIS incident to a fire battalion and a council ward by its x/y point.

Points inside a polygon are assigned directly. Points just outside every polygon
(piers, shoreline, boundary slivers) snap to the nearest one if it is within
SNAP_METERS. Anything farther (bad geocodes like 0,0 or other states) stays
unassigned. Needs census/wards.geojson from fetch_census.py.

Run: python3 assign_incidents.py
  -> neris_incidents_by_area.csv  (one row per incident)
  -> census/calls_by_battalion.csv, census/calls_by_ward.csv
"""
import csv
import math
from collections import defaultdict
from pathlib import Path

from fetch_census import contains, load_zones

ROOT = Path(__file__).resolve().parent
SNAP_METERS = 250
M_PER_DEG_LAT = 111_320
M_PER_DEG_LON = M_PER_DEG_LAT * math.cos(math.radians(40.72))


def seg_dist_m(px, py, ax, ay, bx, by):
    # local equirectangular metres around Jersey City
    px, ax, bx = (v * M_PER_DEG_LON for v in (px, ax, bx))
    py, ay, by = (v * M_PER_DEG_LAT for v in (py, ay, by))
    dx, dy = bx - ax, by - ay
    t = 0 if dx == dy == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def nearest_m(zones, x, y):
    best, name = float("inf"), None
    for z, polys in zones.items():
        for p in polys:
            for ring in p:
                for (ax, ay, *_), (bx, by, *_) in zip(ring, ring[1:]):
                    d = seg_dist_m(x, y, ax, ay, bx, by)
                    if d < best:
                        best, name = d, z
    return name, best


def locate(zones, x, y):
    hit = next((z for z, polys in zones.items() if contains(polys, x, y)), None)
    if hit:
        return hit, "inside"
    name, d = nearest_m(zones, x, y)
    return (name, f"snapped_{d:.0f}m") if d <= SNAP_METERS else ("", "unassigned")


def main():
    layers = {
        "battalion": load_zones(ROOT / "fire-battalions.geojson", "battalion"),
        "ward": load_zones(ROOT / "census" / "wards.geojson", "ward", lambda v: f"Ward {v}"),
    }
    with open(ROOT / "neris_jersey_city_incidents.csv", newline="") as f:
        incidents = list(csv.DictReader(f))

    out, method_counts = [], defaultdict(lambda: defaultdict(int))
    for r in incidents:
        x, y = float(r["x"] or 0), float(r["y"] or 0)
        row = {"ObjectId": r["ObjectId"], "neris_id_incident": r["neris_id_incident"],
               "call_create_eastern": r["call_create_eastern"], "type_1": r["type_1"],
               "type_group": r["type_1"].split("||")[0], "unit_response_count": r["unit_response_count"],
               "duration": r["duration"], "x": r["x"], "y": r["y"]}
        for layer, zones in layers.items():
            zone, method = locate(zones, x, y)
            row[layer], row[f"{layer}_method"] = zone, method
            method_counts[layer]["inside" if method == "inside" else
                                 "snapped" if method.startswith("snapped") else "unassigned"] += 1
        out.append(row)

    with open(ROOT / "neris_incidents_by_area.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)

    for layer in layers:
        pop = {r["area"]: int(r["population"])
               for r in csv.DictReader(open(ROOT / "census" / f"census_by_{layer}.csv"))}
        agg = defaultdict(lambda: defaultdict(float))
        for r in out:
            a = agg[r[layer] or "Unassigned"]
            a["calls"] += 1
            a["unit_responses"] += float(r["unit_response_count"] or 0)
            a["fire_calls"] += r["type_group"] == "FIRE"
            a["non_emergency_calls"] += r["type_group"] == "NOEMERG"
            a["false_alarm_calls"] += r["type_1"].startswith("NOEMERG||FALSE_ALARM")
        rows = []
        for area in sorted(agg, key=lambda a: (a == "Unassigned", a)):
            a, p = agg[area], pop.get(area)
            rows.append({"area": area, "population": p or "",
                         **{k: int(v) for k, v in a.items()},
                         "calls_per_1k": round(1000 * a["calls"] / p, 1) if p else "",
                         "fire_calls_per_1k": round(1000 * a["fire_calls"] / p, 2) if p else "",
                         "false_alarms_per_1k": round(1000 * a["false_alarm_calls"] / p, 1) if p else "",
                         "pct_non_emergency": round(100 * a["non_emergency_calls"] / a["calls"], 1)})
        with open(ROOT / "census" / f"calls_by_{layer}.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(f"{layer}: {dict(method_counts[layer])}")


if __name__ == "__main__":
    main()
