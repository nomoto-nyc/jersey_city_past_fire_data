"""Build 24-hour histograms of NERIS call creation times as standalone SVGs in svgs/."""
import csv
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "svgs"
ORANGE = "#E03E1A"
INK, MUTED, GRID = "#1A1A1A", "#6B6B6B", "#E6E6E6"
W, H = 960, 520
L, R, T, B = 72, 24, 96, 64  # plot margins


def hours(shift_by_offset=False):
    counts = Counter()
    with open(ROOT / "neris_jersey_city_incidents.csv", newline="") as f:
        for row in csv.DictReader(f):
            ts = datetime.fromisoformat(row["call_create_eastern"])
            if shift_by_offset:  # undo a double timezone conversion
                ts = ts + -ts.utcoffset()
            counts[ts.hour] += 1
    return [counts[h] for h in range(24)], sum(counts.values())


def label(h):
    return {0: "12a", 12: "12p"}.get(h, f"{h % 12}{'a' if h < 12 else 'p'}")


def svg(counts, total, title, subtitle):
    pw, ph = W - L - R, H - T - B
    top = max(counts)
    step = 100 if top <= 1000 else 200
    ymax = -(-top // step) * step
    slot = pw / 24
    gap = 2
    bw = slot - gap
    y = lambda v: T + ph - v / ymax * ph
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'font-family="Inter, Helvetica, Arial, sans-serif" role="img" aria-label="{title}">',
        f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>',
        f'<text x="{L}" y="40" font-size="22" font-weight="600" fill="{INK}">{title}</text>',
        f'<text x="{L}" y="66" font-size="14" fill="{MUTED}">{subtitle}</text>',
    ]
    for v in range(0, ymax + 1, step):
        parts.append(f'<line x1="{L}" x2="{W - R}" y1="{y(v):.1f}" y2="{y(v):.1f}" '
                     f'stroke="{GRID if v else "#BDBDBD"}" stroke-width="1"/>')
        parts.append(f'<text x="{L - 10}" y="{y(v) + 4:.1f}" font-size="12" fill="{MUTED}" '
                     f'text-anchor="end">{v:,}</text>')
    peak = counts.index(top)
    low = counts.index(min(counts))
    for h, v in enumerate(counts):
        x = L + h * slot + gap / 2
        yt, hgt = y(v), ph * v / ymax
        r = min(4, hgt)
        # bar with 4px rounded top, square at baseline
        d = (f"M{x:.1f},{T + ph:.1f}V{yt + r:.1f}Q{x:.1f},{yt:.1f} {x + r:.1f},{yt:.1f}"
             f"H{x + bw - r:.1f}Q{x + bw:.1f},{yt:.1f} {x + bw:.1f},{yt + r:.1f}V{T + ph:.1f}Z")
        parts.append(f'<path d="{d}" fill="{ORANGE}"><title>{label(h)}–{label((h + 1) % 24)}: '
                     f'{v:,} calls ({v / total:.1%})</title></path>')
        if h % 3 == 0:
            parts.append(f'<text x="{x + bw / 2:.1f}" y="{T + ph + 20}" font-size="12" '
                         f'fill="{MUTED}" text-anchor="middle">{label(h)}</text>')
        if h in (peak, low):
            parts.append(f'<text x="{x + bw / 2:.1f}" y="{yt - 8:.1f}" font-size="12" '
                         f'font-weight="600" fill="{INK}" text-anchor="middle">{v:,}</text>')
    parts.append(f'<text x="{L + pw / 2}" y="{H - 16}" font-size="12" fill="{MUTED}" '
                 f'text-anchor="middle">Hour call was created (Eastern)</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    OUT.mkdir(exist_ok=True)
    span = "Jan 31 – Sep 16, 2026"
    counts, total = hours()
    (OUT / "calls_by_hour.svg").write_text(svg(
        counts, total, "Jersey City Fire calls by hour of day",
        f"{total:,} NERIS incidents, {span} · call_create_eastern"))
    counts, total = hours(shift_by_offset=True)
    (OUT / "calls_by_hour_offset_corrected.svg").write_text(svg(
        counts, total, "Jersey City Fire calls by hour of day (offset-corrected)",
        f"{total:,} NERIS incidents, {span} · call_create read as local wall-clock time"))


if __name__ == "__main__":
    main()
