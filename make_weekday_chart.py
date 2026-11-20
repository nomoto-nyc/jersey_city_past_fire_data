"""Calls per day by day of week (every day as a dot, median as a bar) -> svgs/calls_by_weekday.svg.

Uses offset-corrected local time (see calls_by_hour_offset_corrected.svg) and only full
days, Feb 1 - Sep 15, 2026.
"""
import csv
import random
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from statistics import median

ROOT = Path(__file__).parent
ORANGE, DOT = "#E03E1A", "#F2A08A"
INK, MUTED, GRID = "#111827", "#6B7280", "#E5E7EB"
START, END = date(2026, 2, 1), date(2026, 9, 15)
NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def daily_counts():
    counts = Counter()
    with open(ROOT / "neris_jersey_city_incidents.csv", newline="") as f:
        for r in csv.DictReader(f):
            ts = datetime.fromisoformat(r["call_create_eastern"])
            counts[(ts - ts.utcoffset()).date()] += 1
    days = [START + timedelta(n) for n in range((END - START).days + 1)]
    return {d: counts[d] for d in days}


def main():
    daily = daily_counts()
    by_dow = [[(d, n) for d, n in daily.items() if d.weekday() == i] for i in range(7)]
    W, H = 960, 580
    L, R, T, B = 72, 24, 110, 90
    pw, ph = W - L - R, H - T - B
    ymax = 160
    y = lambda v: T + ph - v / ymax * ph
    slot = pw / 7
    rnd = random.Random(7)
    total_days = len(daily)
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="Inter, -apple-system, Helvetica, Arial, sans-serif" role="img" '
         f'aria-label="Calls per day by day of week">',
         f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>',
         f'<text x="{L}" y="44" font-size="24" font-weight="600" fill="{INK}">Calls per day, by day of week</text>',
         f'<text x="{L}" y="72" font-size="14" fill="{MUTED}">Each dot is one day ({total_days} days, '
         f'Feb 1 – Sep 15, 2026). Bar = median day. Jersey City Fire, NERIS Public.</text>']
    for v in range(0, ymax + 1, 40):
        o.append(f'<line x1="{L}" x2="{W - R}" y1="{y(v):.1f}" y2="{y(v):.1f}" '
                 f'stroke="{GRID if v else "#BDBDBD"}" stroke-width="1"/>')
        o.append(f'<text x="{L - 10}" y="{y(v) + 4:.1f}" font-size="12" fill="{MUTED}" text-anchor="end">{v}</text>')
    outliers = sorted(daily.items(), key=lambda kv: -kv[1])[:2]
    for i, days in enumerate(by_dow):
        cx = L + slot * (i + 0.5)
        med = median(n for _, n in days)
        bw = slot * 0.56
        top = y(med)
        o.append(f'<path d="M{cx - bw / 2:.1f},{y(0):.1f}V{top + 4:.1f}Q{cx - bw / 2:.1f},{top:.1f} '
                 f'{cx - bw / 2 + 4:.1f},{top:.1f}H{cx + bw / 2 - 4:.1f}Q{cx + bw / 2:.1f},{top:.1f} '
                 f'{cx + bw / 2:.1f},{top + 4:.1f}V{y(0):.1f}Z" fill="{ORANGE}" fill-opacity="0.16">'
                 f'<title>{NAMES[i]}: median {med:g} calls/day</title></path>')
        o.append(f'<line x1="{cx - bw / 2:.1f}" x2="{cx + bw / 2:.1f}" y1="{top:.1f}" y2="{top:.1f}" '
                 f'stroke="{ORANGE}" stroke-width="3" stroke-linecap="round"/>')
        for d, n in days:
            jx = cx + rnd.uniform(-bw * 0.38, bw * 0.38)
            o.append(f'<circle cx="{jx:.1f}" cy="{y(n):.1f}" r="4" fill="{DOT}" fill-opacity="0.85" '
                     f'stroke="#FFFFFF" stroke-width="1"><title>{d:%a %b %-d}: {n} calls</title></circle>')
            if (d, n) in outliers:
                o.append(f'<text x="{jx + 9:.1f}" y="{y(n) + 4:.1f}" font-size="12" fill="{MUTED}">'
                         f'{d:%b %-d} · {n}</text>')
        o.append(f'<text x="{cx:.1f}" y="{y(0) + 22:.1f}" font-size="13" fill="{MUTED}" '
                 f'text-anchor="middle">{NAMES[i]}</text>')
        o.append(f'<text x="{cx:.1f}" y="{y(0) + 42:.1f}" font-size="15" font-weight="600" fill="{INK}" '
                 f'text-anchor="middle">{med:g}</text>')
    o.append(f'<text x="{L}" y="{H - 16}" font-size="12" fill="{MUTED}">Times use call_create read as local '
             f'clock time (offset-corrected).</text>')
    o.append("</svg>")
    out = ROOT / "svgs" / "calls_by_weekday.svg"
    out.write_text("\n".join(o))
    print(out, [median(n for _, n in d) for d in by_dow])


if __name__ == "__main__":
    main()
