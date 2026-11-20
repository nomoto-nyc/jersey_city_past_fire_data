"""Pull the latest ACS 5-year tract data for Jersey City and roll it up to fire
battalions and council wards.

How tracts are split: census tracts don't line up with battalion or ward lines, so
each tract is split by its 2020 census blocks. Every block's interior point is placed
in a battalion and a ward (point-in-polygon), and a tract's share of each area is the
share of its 2020 block population living there. Counts (people, households, housing
units...) are apportioned by those shares; rates are recomputed from the apportioned
counts. Medians can't be apportioned, so median income stays tract-only and areas get
income-bracket shares (households under $50k, $200k+) instead.

Sources (no API key needed):
  ACS:     Census Reporter API, "latest" release (mirrors the Census Bureau ACS tables)
  Blocks:  Census TIGERweb, 2020 Census Blocks (POP100, HU100, interior point)
  Wards:   data.jerseycitynj.gov "jersey-city-ward-and-councilperson-map"
  Battalions: fire-battalions.geojson (data.jerseycitynj.gov "fire-battalions")

Run: python3 fetch_census.py   -> writes census/
"""
import csv
import json
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "census"
PLACE = "16000US3436000"  # Jersey City city, NJ
CR_URL = "https://api.censusreporter.org/1.0/data/show/latest"
BLOCKS_URL = ("https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
              "Tracts_Blocks/MapServer/2/query")
WARDS_URL = ("https://data.jerseycitynj.gov/api/explore/v2.1/catalog/datasets/"
             "jersey-city-ward-and-councilperson-map/exports/geojson")


def cols(table, *nums):
    return [f"{table}{n:03d}" for n in nums]


# Count measures: name -> ACS columns summed. Every one is additive, so it can be
# apportioned to battalions and wards.
COUNTS = {
    "population": cols("B01003", 1),
    "age_under_5": cols("B01001", 3, 27),
    "age_65_plus": cols("B01001", *range(20, 26), *range(44, 50)),
    "poverty_universe": cols("B17001", 1),
    "below_poverty": cols("B17001", 2),
    "households": cols("B11001", 1),
    "income_universe": cols("B19001", 1),
    "hh_income_under_50k": cols("B19001", *range(2, 11)),
    "hh_income_200k_plus": cols("B19001", 17),
    "occupied_units": cols("B25003", 1),
    "renter_occupied": cols("B25003", 3),
    "housing_units": cols("B25001", 1),
    "units_in_20plus_buildings": cols("B25024", 8, 9),
    "units_built_pre_1940": cols("B25034", 11),
    "language_universe": cols("C16002", 1),
    "limited_english_households": cols("C16002", 4, 7, 10, 13),
}
# Rates: name -> (numerator, denominator), recomputed after apportioning.
RATES = {
    "pct_under_5": ("age_under_5", "population"),
    "pct_65_plus": ("age_65_plus", "population"),
    "pct_below_poverty": ("below_poverty", "poverty_universe"),
    "pct_hh_under_50k": ("hh_income_under_50k", "income_universe"),
    "pct_hh_200k_plus": ("hh_income_200k_plus", "income_universe"),
    "pct_renter": ("renter_occupied", "occupied_units"),
    "pct_units_20plus_bldg": ("units_in_20plus_buildings", "housing_units"),
    "pct_built_pre_1940": ("units_built_pre_1940", "housing_units"),
    "pct_limited_english_hh": ("limited_english_households", "language_universe"),
}
TABLES = sorted({c[:6] for v in COUNTS.values() for c in v} | {"B19013"})


def get_json(url, tries=4):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "jc-fire-data-script"})
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except (OSError, ValueError):
            if attempt == tries - 1:
                raise
            time.sleep(2 ** attempt)


# ---- ACS --------------------------------------------------------------------------
def fetch_acs():
    data, release = {}, None
    for i in range(0, len(TABLES), 4):  # a few tables per request keeps responses small
        q = urllib.parse.urlencode({"table_ids": ",".join(TABLES[i:i + 4]), "geo_ids": f"140|{PLACE}"})
        d = get_json(f"{CR_URL}?{q}")
        if "error" in d:
            raise RuntimeError(d["error"])
        release = d["release"]
        for geo, tables in d["data"].items():
            for t in tables.values():
                data.setdefault(geo, {}).update(t["estimate"])
    tracts = {}
    for geo, est in data.items():
        tract = geo.split("US")[1]  # 11-digit tract GEOID
        row = {k: int(sum(est.get(c) or 0 for c in v)) for k, v in COUNTS.items()}
        row["median_hh_income"] = est.get("B19013001")
        tracts[tract] = row
    return tracts, release


# ---- Blocks -----------------------------------------------------------------------
def fetch_blocks(tract_ids):
    counties = sorted({t[:5] for t in tract_ids})
    blocks = []
    for c in counties:
        offset = 0
        while True:
            q = urllib.parse.urlencode({
                "where": f"STATE='{c[:2]}' AND COUNTY='{c[2:]}'",
                "outFields": "GEOID,POP100,HU100,INTPTLAT,INTPTLON",
                "returnGeometry": "false", "f": "json",
                "resultOffset": offset, "resultRecordCount": 2000, "orderByFields": "GEOID"})
            feats = get_json(f"{BLOCKS_URL}?{q}")["features"]
            for f in feats:
                a = f["attributes"]
                if a["GEOID"][:11] in tract_ids:
                    blocks.append({"geoid": a["GEOID"], "tract": a["GEOID"][:11],
                                   "pop": a["POP100"] or 0, "hu": a["HU100"] or 0,
                                   "lat": float(a["INTPTLAT"]), "lon": float(a["INTPTLON"])})
            if len(feats) < 2000:
                break
            offset += 2000
    return blocks


# ---- Geometry (stdlib point-in-polygon) ---------------------------------------------
def polygons(geom):
    """List of polygons, each a list of rings [(lon, lat), ...]."""
    if geom["type"] == "Polygon":
        return [geom["coordinates"]]
    if geom["type"] == "MultiPolygon":
        return geom["coordinates"]
    raise ValueError(geom["type"])


def in_ring(x, y, ring):
    inside, j = False, len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i][:2]
        xj, yj = ring[j][:2]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def contains(polys, x, y):
    return any(in_ring(x, y, p[0]) and not any(in_ring(x, y, h) for h in p[1:]) for p in polys)


def nearest(zones, x, y):
    best, name = float("inf"), None
    for zname, polys in zones.items():
        for p in polys:
            for vx, vy in (pt[:2] for pt in p[0]):
                d = (vx - x) ** 2 + (vy - y) ** 2
                if d < best:
                    best, name = d, zname
    return name


def load_zones(path, key, fmt=lambda v: v):
    gj = json.loads(Path(path).read_text())
    return {fmt(f["properties"][key]): polygons(f["geometry"]) for f in gj["features"]}


def assign(blocks, zones, field):
    snapped = 0
    for b in blocks:
        hit = next((z for z, polys in zones.items() if contains(polys, b["lon"], b["lat"])), None)
        if hit is None:
            hit = nearest(zones, b["lon"], b["lat"])
            snapped += b["pop"]
        b[field] = hit
    return snapped


# ---- Apportion --------------------------------------------------------------------
def crosswalk(blocks, field):
    """tract -> {zone: weight}; weights by 2020 population, then housing units, then block count."""
    out = {}
    by_tract = defaultdict(list)
    for b in blocks:
        by_tract[b["tract"]].append(b)
    for tract, bs in by_tract.items():
        for basis in ("pop", "hu", None):
            totals = defaultdict(float)
            for b in bs:
                totals[b[field]] += b[basis] if basis else 1
            s = sum(totals.values())
            if s:
                out[tract] = {z: v / s for z, v in totals.items()}
                break
    return out


def rollup(tracts, xwalk):
    zones = defaultdict(lambda: defaultdict(float))
    for tract, weights in xwalk.items():
        for z, w in weights.items():
            for k in COUNTS:
                zones[z][k] += tracts.get(tract, {}).get(k, 0) * w
    rows = []
    for z in sorted(zones):
        r = {"area": z, **{k: round(v) for k, v in zones[z].items()}}
        for name, (num, den) in RATES.items():
            r[name] = round(100 * zones[z][num] / zones[z][den], 1) if zones[z][den] else None
        rows.append(r)
    return rows


def write_csv(path, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main():
    OUT.mkdir(exist_ok=True)
    tracts, release = fetch_acs()
    print(f"ACS: {release['name']} ({release['years']}), {len(tracts)} tracts")

    wards_path = OUT / "wards.geojson"
    wards_path.write_text(json.dumps(get_json(WARDS_URL)))
    wards = load_zones(wards_path, "ward", lambda v: f"Ward {v}")
    battalions = load_zones(ROOT / "fire-battalions.geojson", "battalion")
    print(f"Zones: {len(battalions)} battalions, {len(wards)} wards")

    blocks = fetch_blocks(set(tracts))
    pop2020 = sum(b["pop"] for b in blocks)
    print(f"Blocks: {len(blocks):,} (2020 population {pop2020:,})")
    for field, zones in (("battalion", battalions), ("ward", wards)):
        snapped = assign(blocks, zones, field)
        print(f"  {field}: {snapped:,} people in blocks outside every polygon, snapped to nearest")

    xw = {f: crosswalk(blocks, f) for f in ("battalion", "ward")}
    tract_rows, xw_rows = [], []
    for t in sorted(tracts):
        row = {"tract_geoid": t, **tracts[t]}
        for f in ("battalion", "ward"):
            w = xw[f].get(t, {})
            main_zone = max(w, key=w.get) if w else None
            row[f"main_{f}"] = main_zone
            row[f"main_{f}_share"] = round(w[main_zone], 3) if w else None
            xw_rows += [{"tract_geoid": t, "layer": f, "area": z, "weight": round(v, 4)}
                        for z, v in sorted(w.items(), key=lambda kv: -kv[1])]
        tract_rows.append(row)
    write_csv(OUT / "acs_tracts.csv", tract_rows)
    write_csv(OUT / "tract_crosswalk.csv", xw_rows)
    write_csv(OUT / "blocks_2020.csv", blocks)
    for f in ("battalion", "ward"):
        write_csv(OUT / f"census_by_{f}.csv", rollup(tracts, xw[f]))
    (OUT / "README.json").write_text(json.dumps({
        "acs_release": release, "tracts": len(tracts), "blocks_2020": len(blocks),
        "block_population_2020": pop2020, "method": __doc__.split("Sources")[0].strip(),
    }, indent=2) + "\n")
    print(f"Wrote {OUT}/")


if __name__ == "__main__":
    main()
