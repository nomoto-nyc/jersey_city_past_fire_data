"""Tree-card SVGs breaking down NERIS calls -> svgs/nonemergency_tree.svg, svgs/emergency_tree.svg."""
import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
ORANGE, ORANGE_SOFT, TINT = "#E03E1A", "#F2A08A", "#FFF5F0"
INK, MUTED, LINE, TRACK, CARD_LINE, NAVY = "#111827", "#6B7280", "#CBD5E1", "#E5E7EB", "#E2E8F0", "#111827"
SPAN = "Jersey City Fire · Feb 1 – Sep 16, 2026"

# Non-emergency: (NERIS subtypes, eyebrow, display name lines)
NONEMERG = [
    (["MALFUNCTIONING_ALARM"], "Alarm system", ["Malfunctioning", "alarm"]),
    (["ACCIDENTAL_ALARM"], "Alarm system", ["Accidental", "alarm"]),
    (["NO_INCIDENT_FOUND_LOCATION_ERROR", "SMOKE_FROM_NONHOSTILE_SOURCE",
      "INVESTIGATE_HAZARDOUS_RELEASE", "CONTROLLED_BURNING_AUTHORIZED"], "Good faith", ["Good intent"]),
    (["OTHER_FALSE_CALL"], "Unclassified", ["Other false", "call"]),
    (["INTENTIONAL_FALSE_ALARM", "BOMB_SCARE"], "Deliberate", ["Intentional /", "bomb scare"]),
    (["CANCELLED"], "Good faith", ["Cancelled"]),
]

# Emergency: top-level NERIS group -> (display name lines, {subtype: short label for eyebrow})
EMERG = {
    "PUBSERV": (["Public", "service"], {"CITIZEN_ASSIST_SERVICE_CALL": "citizen assist"}),
    "HAZSIT": (["Hazardous", "situation"], {"GAS_LEAK_ODOR": "gas leak / odor"}),
    "FIRE": (["Fire"], {"CONFINED_COOKING_APPLIANCE_FIRE": "cooking fires"}),
    "MEDICAL": (["Medical"], {"MOTOR_VEHICLE_COLLISION": "vehicle collisions"}),
    "RESCUE": (["Rescue"], {"ELEVATOR_ESCALATOR_RESCUE": "elevator rescues"}),
    "LAWENFORCE": (["Law", "enforcement"], {}),
}


def load():
    with open(ROOT / "neris_jersey_city_incidents.csv", newline="") as f:
        return [(r["type_1"].split("||"), int(r["unit_response_count"])) for r in csv.DictReader(f)]


def nonemergency_rows(rows):
    calls, units = defaultdict(int), defaultdict(int)
    for parts, u in rows:
        if parts[0] == "NOEMERG":
            calls[parts[-1]] += 1
            units[parts[-1]] += u
    out = [(sum(calls[k] for k in keys), sum(units[k] for k in keys), eyebrow, name)
           for keys, eyebrow, name in NONEMERG]
    assert sum(r[0] for r in out) == sum(calls.values()), "a NOEMERG subtype is missing"
    return out


def emergency_rows(rows):
    calls, units, subs = Counter(), Counter(), defaultdict(Counter)
    for parts, u in rows:
        if parts[0] != "NOEMERG":
            calls[parts[0]] += 1
            units[parts[0]] += u
            subs[parts[0]][parts[-1]] += 1
    assert set(calls) == set(EMERG), f"unexpected groups: {set(calls) ^ set(EMERG)}"
    out = []
    for g, (name, labels) in EMERG.items():
        if labels:
            sub, label = next(iter(labels.items()))
            eyebrow = f"{subs[g][sub] / calls[g]:.0%} {label}"
        else:
            eyebrow = "Assisting police"
        out.append((calls[g], units[g], eyebrow, name))
    return out


def render(cards, total, root_label, title, subtitle, footnote, out_name):
    cards = sorted(cards, key=lambda r: -r[0])
    n_all, u_all = sum(r[0] for r in cards), sum(r[1] for r in cards)
    W, H = 1440, 760
    cw, ch, gap = 208, 268, 20
    x0 = (W - (6 * cw + 5 * gap)) / 2
    card_y, rail_y = 400, 330
    root_w, root_h, root_y = 300, 74, 176
    root_x = (W - root_w) / 2
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="Inter, -apple-system, Helvetica, Arial, sans-serif" role="img" aria-label="{title}">',
         f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>',
         f'<text x="{x0}" y="60" font-size="30" font-weight="600" fill="{INK}">{title}</text>',
         f'<text x="{x0}" y="94" font-size="17" fill="{MUTED}">'
         f'{subtitle.format(n=n_all, share=n_all / total, units=u_all)} · {SPAN}</text>',
         f'<rect x="{root_x}" y="{root_y}" width="{root_w}" height="{root_h}" rx="12" fill="{NAVY}"/>',
         f'<circle cx="{root_x + 40}" cy="{root_y + 30}" r="7" fill="{ORANGE}"/>',
         f'<text x="{root_x + 58}" y="{root_y + 38}" font-size="24" font-weight="600" fill="#FFFFFF">{root_label}</text>',
         f'<text x="{root_x + 58}" y="{root_y + 60}" font-size="14" fill="#CBD5E1">{n_all:,} calls</text>',
         f'<line x1="{W / 2}" x2="{W / 2}" y1="{root_y + root_h}" y2="{rail_y}" stroke="{LINE}" stroke-width="2"/>',
         f'<line x1="{x0 + cw / 2}" x2="{x0 + 5 * (cw + gap) + cw / 2}" y1="{rail_y}" y2="{rail_y}" '
         f'stroke="{LINE}" stroke-width="2"/>']
    bar_w = cw - 48
    for i, (n, u, eyebrow, name) in enumerate(cards):
        x = x0 + i * (cw + gap)
        cx, hi = x + cw / 2, i == 0
        share = n / n_all
        o.append(f'<line x1="{cx}" x2="{cx}" y1="{rail_y}" y2="{card_y}" stroke="{LINE}" stroke-width="2"/>')
        o.append(f'<g><title>{" ".join(name)}: {n:,} calls ({share:.1%}), {u:,} unit responses</title>')
        o.append(f'<rect x="{x}" y="{card_y}" width="{cw}" height="{ch}" rx="16" '
                 f'fill="{TINT if hi else "#FFFFFF"}" stroke="{ORANGE_SOFT if hi else CARD_LINE}" stroke-width="2"/>')
        o.append(f'<text x="{x + 24}" y="{card_y + 40}" font-size="14" fill="{ORANGE if hi else MUTED}">{eyebrow}</text>')
        for j, line in enumerate(name):
            o.append(f'<text x="{x + 24}" y="{card_y + 74 + j * 26}" font-size="20" font-weight="600" '
                     f'fill="{INK}">{line}</text>')
        pct = f"{share:.0%}" if share >= 0.1 else f"{share:.1%}"
        o.append(f'<text x="{x + 24}" y="{card_y + 186}" font-size="46" font-weight="600" '
                 f'fill="{ORANGE if hi else INK}">{pct}</text>')
        o.append(f'<rect x="{x + 24}" y="{card_y + 206}" width="{bar_w}" height="8" rx="4" fill="{TRACK}"/>')
        o.append(f'<rect x="{x + 24}" y="{card_y + 206}" width="{max(8, bar_w * share):.1f}" height="8" rx="4" '
                 f'fill="{ORANGE if hi else ORANGE_SOFT}"/>')
        o.append(f'<text x="{x + 24}" y="{card_y + 244}" font-size="15" fill="{MUTED}">{n:,} calls · {u:,} units</text>')
        o.append('</g>')
    o.append(f'<text x="{x0}" y="{H - 30}" font-size="15" fill="{MUTED}">{footnote} Largest share on the left.</text>')
    o.append('</svg>')
    (ROOT / "svgs" / out_name).write_text("\n".join(o))


def main():
    rows = load()
    total = len(rows)
    render(nonemergency_rows(rows), total, "Non-emergency", "What non-emergency calls are made of",
           "Share of {n:,} non-emergency calls ({share:.0%} of all calls, {units:,} unit responses)",
           "NERIS Public, Jersey City Fire Department. Good intent = no incident found, harmless smoke, "
           "hazmat investigation, authorized burn.", "nonemergency_tree.svg")
    render(emergency_rows(rows), total, "Emergency", "What emergency and service calls are made of",
           "Share of {n:,} calls not coded non-emergency ({share:.0%} of all calls, {units:,} unit responses)",
           "NERIS Public, Jersey City Fire Department. Small label = largest subtype within each group. "
           "Public service includes non-medical alarm activations.", "emergency_tree.svg")


if __name__ == "__main__":
    main()
