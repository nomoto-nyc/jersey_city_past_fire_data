"""Low / mid / high estimate of what NERIS false-alarm responses cost Jersey City Fire.

Every input below is an assumption unless marked SOURCED. Change them here, re-run,
and the whole estimate updates. Run: python3 false_alarm_cost.py
"""
import csv
from datetime import datetime
from pathlib import Path
from statistics import median

ROOT = Path(__file__).parent

# ---- SOURCED ------------------------------------------------------------------
FIRE_BUDGET = 81_930_000        # Hudson County View budget hearing coverage
PERSONNEL_SHARE = 0.94          # same source: ~94% is salaries and benefits
COMPANIES = 28                  # jerseycitynj.gov/JCFD: 28 companies on duty daily
HOURS_PER_YEAR = 8_760

# ---- ASSUMPTIONS (low, mid, high) ------------------------------------------------
SCENARIOS = {
    # Benefits (PFRS pension, health) sit outside the department line in NJ budgets.
    # Multiplier on the personnel share to reach fully loaded cost.
    "benefit_load":   (1.00, 1.25, 1.45),
    # Share of the recorded incident duration an average unit is committed
    # (first-due units stay to the end; extra units are often released early).
    "unit_share":     (0.60, 0.80, 1.00),
    "return_min":     (4, 6, 8),        # drive back to quarters, not in `duration`
    "dispatch_min":   (2, 3, 4),        # call-taker/dispatcher time per incident
    "dispatch_rate":  (50, 65, 80),     # $/hr fully loaded dispatcher
    "miles_per_unit": (2.0, 3.0, 4.0),  # round trip per unit
    "mpg":            (5.0, 4.0, 3.0),  # apparatus fuel economy
    "idle_gph":       (0.8, 1.0, 1.2),  # gallons/hour idling on scene
    "diesel":         (3.75, 4.00, 4.50),
    "wear_per_mile":  (1.50, 2.50, 4.00),  # maintenance + mileage depreciation
}

SYSTEM = {"MALFUNCTIONING_ALARM", "ACCIDENTAL_ALARM"}
ABUSE = {"INTENTIONAL_FALSE_ALARM", "BOMB_SCARE"}


def load():
    rows = list(csv.DictReader(open(ROOT / "neris_jersey_city_incidents.csv", newline="")))
    times = [datetime.fromisoformat(r["call_create_eastern"]) for r in rows]
    days = (max(times) - min(times)).total_seconds() / 86_400
    fa = [r for r in rows if r["type_1"].startswith("NOEMERG||FALSE_ALARM")]
    fill = median(float(r["duration"]) for r in fa if float(r["duration"]) > 0)
    for r in fa:  # 0-second durations are missing values, not instant calls
        r["dur_h"] = (float(r["duration"]) or fill) / 3600
        r["units"] = int(r["unit_response_count"])
        r["sub"] = r["type_1"].split("||")[2]
    return fa, days


def cost(calls, i):
    a = {k: v[i] for k, v in SCENARIOS.items()}
    # Personnel only: the other ~6% (other expenses: fuel, maintenance, supplies) is
    # costed per call below, so including it here would count it twice.
    budget = FIRE_BUDGET * PERSONNEL_SHARE * a["benefit_load"]
    rate = budget / (COMPANIES * HOURS_PER_YEAR)
    unit_hours = sum(c["units"] * (c["dur_h"] * a["unit_share"] + a["return_min"] / 60) for c in calls)
    responses = sum(c["units"] for c in calls)
    scene_hours = sum(c["units"] * c["dur_h"] * a["unit_share"] for c in calls)
    fuel_gal = responses * a["miles_per_unit"] / a["mpg"] + scene_hours * a["idle_gph"]
    out = {
        "Crew & apparatus time": unit_hours * rate,
        "Dispatch": len(calls) * a["dispatch_min"] / 60 * a["dispatch_rate"],
        "Fuel": fuel_gal * a["diesel"],
        "Vehicle wear": responses * a["miles_per_unit"] * a["wear_per_mile"],
    }
    return out, unit_hours, rate


def main():
    fa, days = load()
    scale = 365 / days
    groups = {
        "Alarm-system problems (malfunctioning + accidental)": [c for c in fa if c["sub"] in SYSTEM],
        "All NERIS false alarms": fa,
    }
    print(f"Data window: {days:.0f} days; annualised x{scale:.2f}\n")
    for name, calls in groups.items():
        print(f"== {name}: {len(calls):,} calls, {sum(c['units'] for c in calls):,} unit responses")
        for i, label in enumerate(("Low", "Mid", "High")):
            parts, uh, rate = cost(calls, i)
            total = sum(parts.values())
            share = uh / (COMPANIES * HOURS_PER_YEAR * days / 365)
            print(f"  {label:4} ${rate:,.0f}/company-hr | {uh:,.0f} unit-hrs "
                  f"({share:.1%} of company capacity) | window ${total/1e6:.2f}M | "
                  f"annual ${total*scale/1e6:.2f}M | per call ${total/len(calls):,.0f}")
            print("       " + "  ".join(f"{k}: ${v*scale/1e3:,.0f}k" for k, v in parts.items()))
        print()


if __name__ == "__main__":
    main()
