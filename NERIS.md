# Jersey City NERIS Public extract

Run `python3 fetch_neris.py` to refresh `neris_jersey_city_incidents.csv` and
`neris_jersey_city_summary.json` from the [NERIS Public Incident Basics ArcGIS
layer](https://lpbcyjocolyzmvo6.svcs5.arcgis.com/lPbcyJOcoLyZmvo6/ArcGIS/rest/services/NERIS%20Public%20Incident%20Basics/FeatureServer/0).
The script filters on Jersey City Fire Department NERIS ID `FD34017554`, fetches
all pages, and verifies the record count and unique ArcGIS object IDs.

The extract retrieved November 18, 2026 contains 10,777 incidents dated January
31 through September 16, 2026 (Eastern time). It includes `unit_response_count`,
the number of unit responses recorded for each incident. Summing that field
counts deployments to incidents, not distinct vehicles or companies. The public
layer does not expose individual unit names, apparatus IDs, staffing, or unit
dispatch/arrival times. The U.S. Fire Administration says the incident layer is
published with a 60-day delay and excludes detailed unit response data.

The extract also carries every other public field: `x`/`y` points (rounded to
about 10 m; 99% fall inside Jersey City, about 99 are bad geocodes such as 0,0 or
other states), `civic_location` (state + ZIP), location use, smoke-alarm and
suppression fields, room of origin, building damage, displacement, actions and
tactics, and hazard flags. Most detail fields are sparse. Smoke-alarm presence is
filled for about 71% of fire incidents, but room of origin and building damage only
for about 3%.

The extract is **department-reported**, not a strict geographic filter for Jersey
City. County is missing on 207 rows; one row lists Essex County. Dates reflect
available NERIS Public records, not complete 2026 activity. The January and
September months in particular are partial.

Sources: [USFA NERIS Public](https://www.usfa.fema.gov/neris/public/),
[USFA announcement](https://www.usfa.fema.gov/blog/neris-public-transparent-fire-incident-data/).
