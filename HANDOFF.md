# Handoff: Jersey City fire calls map (2014–2023)

## Goal
A lightweight, single-file HTML map of Jersey City fire department calls, to be published on GitHub Pages. Combines 2014–2017 workbooks with the 2018, 2019–2022 and 2023 open-data exports.

## Current state
- **`index.html`** (project root): the finished map. Four fire battalions shaded by calls or units responded. Filters for year, call category and measure. Per-battalion year table, coverage notes, data caveats. Generated, not hand-edited.
- **`fire_calls_2014_2023_by_battalion.csv`**: the combined table behind the map (267 rows: year, battalion, category, calls, units, source).
- **`.gitignore`**: contains `.env`, so the CARTO key file is not committed.
- **`HANDOFF.md`**: this file.
- **Nothing is committed or pushed.** `git status` shows all files untracked. The user has not yet asked for a commit.
- Other untracked files already in the folder (not created by us, except where noted): `2014-2017.zip`, `fire-battalions.geojson`, `police-districts.geojson`, `jersey_city_censustract_geojson (1).geojson`, `jersey_city_fire.jpeg`, `.vscode/`, `.env`.

## Open decision (blocking publish)
The CARTO basemap needs an API key. The key is embedded in `index.html` as plain text (`?key=` in the tile URL), so it will be public on GitHub Pages. The user has not yet chosen between:
1. Keep the key in the page and restrict it in the CARTO dashboard to the GitHub Pages domain and `localhost`.
2. Remove the key and use a keyless basemap. Keyless CARTO tiles now show an "API KEY REQUIRED" watermark, so a different provider would be needed.

Do not repeat the key value in chat. It lives in `.env` as `carto_api = …`.

## Data sources
| Years | Source | Notes |
|---|---|---|
| 2014, 2015, 2016, 2017 | Local `2014-2017.zip` → four XLSX workbooks | Wide layout: rows are call types, columns are battalion pairs (calls, units), week in col 11, year in col 12. 2015 has 33 weeks, 2017 has 26 (partial). |
| 2018 | API `fire-department-calls-2018` (JSON export) | Only weeks 44–52. Partial. |
| 2019–2022 | API `fire-department-calls-2019-2022` (JSON export) | Only rows with year label 2019–2022 used. Week fields are inconsistent (2021–2022 use `week_number`). |
| 2023 | API `fire-department-calls-2023` (JSON export) | Weeks 1–8 only. Partial. Includes 32 unlabelled-year week-7 rows (202 calls), assigned to 2023. |

Export endpoint pattern: `https://data.jerseycitynj.gov/api/explore/v2.1/catalog/datasets/<dataset-id>/exports/json?lang=en`

Other datasets exist (`fire-battalions`, `fire-house-addresses`, `fire-department-service-calls-aggregated-2014-2017`), but the aggregated 2014–2017 one returned 0 records, so the local zip is the 2014–2017 source.

Key facts about the data:
- Records are weekly counts per battalion and call type. No addresses or coordinates, so the map shades battalion areas.
- The "Other" battalion has no territory and is excluded. Most of its values are inspections and mutual aid. The 2019–2023 "Other" rows have null calls.
- The source's category labels change around 2021, so category shares across that break need care.
- For 2014–2018 I assigned categories by keyword. For 2019–2023 I used the source's `category_type`.
- Non-call activity rows (Training, Registrations, Fire safety events, Fines) and subtotal rows (`TOTAL…`) are skipped.

## Pipeline (scripts in scratchpad)
Scratchpad dir: `/private/tmp/claude-501/-Users-adriankombe--claude-spares-spare-ORP7r4/a48ad35e-fcf0-4a79-a021-893397dd6a27/scratchpad/`
- `raw/` — downloaded JSON exports: `2018.json`, `2019_2022.json`, `2023.json`. Also `2014_2017_api.json` (empty).
- `zip/` — extracted XLSX files.
- `build_data.py` — combines all sources into one CSV. Usage: `python3 build_data.py <raw_dir> <zip_dir> <out_csv>`.
- `template.html` — HTML template with placeholders `/*__ROWS__*/`, `/*__BATT__*/`, `/*__COVERAGE__*/`, and `__CARTO_KEY__`.
- `make_page.py` — computes weeks covered per year, injects data into the template, and writes the page. It reads `CARTO_KEY` from the environment and fails if it's missing.

Rebuild from the project folder:
```bash
S=/private/tmp/claude-501/-Users-adriankombe--claude-spares-spare-ORP7r4/a48ad35e-fcf0-4a79-a021-893397dd6a27/scratchpad
P=/Users/adriankombe/jersey_city_past_fire_data
export CARTO_KEY=$(grep -i '^carto_api' $P/.env | sed -E 's/^[^=]*=[[:space:]]*//; s/["'\'' \r]//g')
python3 $S/build_data.py $S/raw $S/zip $S/combined.csv
python3 $S/make_page.py $S $S/raw $S/zip $S/combined.csv $P/fire-battalions.geojson $S/template.html $P/index.html
cp $S/combined.csv $P/fire_calls_2014_2023_by_battalion.csv
```
The scratchpad is session-specific. Copy the scripts into the project if the work must survive this session.

## Bugs already fixed (don't reintroduce)
- 2014–2017 XLSX: week is column 11 and year is column 12. An earlier off-by-one read the wrong columns.
- Some workbooks have only 13 columns, so use `r.get()` rather than direct indexing.
- Map initially zoomed to level 19 because the first `fitBounds` ran before the container had its final size. Fixed with `invalidateSize()` and `maxZoom: 14`.
- OSM tile server returned 403 for the user (it works from our sandbox). Switched to CARTO basemap.

## Verification done
- Combined totals reconcile. 2023 labelled rows and the 2023 export total 1,922 calls, and with the 202 unlabelled-year calls the total is 2,124.
- Page loads with no console errors. Four battalion polygons render. Year and category filters update the map and totals. Example: 2021 Residential = 3,340 calls.
- CARTO tiles load with the key in the browser pane.

## Known limits / next steps
1. Resolve the API-key decision above before publishing.
2. Commit `index.html` (and CSV, `.gitignore`, optionally `HANDOFF.md`) to `main` only when the user asks. Consider keeping `HANDOFF.md` out of the commit.
3. Enable GitHub Pages. `index.html` at the root serves at the root URL.
4. Possible improvements, not requested: trend chart, per-week view, using the police-districts or census-tract GeoJSON.
