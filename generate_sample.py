"""Generate fictional rack-damage inspection records for the RackScan demo.
Fixed seed -> identical output. Writes data/sample.json.
"""
import json
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 20260924
AS_OF = date(2026, 9, 1)
ROWS = ["A", "B", "C", "D", "E", "F"]
BAYS = 12           # bays per row -> frames 1..13
LEVELS = 4          # beam levels 1..4
N_ISSUES = 46

# component, location kind, weight, typical descriptions
COMPONENTS = [
    ("Upright", "frame", 34, ["Front upright dented at forklift height", "Upright bent in aisle direction",
                              "Upright twisted, section deformed", "Paint scrape with minor dent"]),
    ("Base plate", "frame", 10, ["Base plate bent", "Base plate lifted from floor"]),
    ("Anchor", "frame", 8, ["Anchor bolt missing", "Anchor loose", "Anchor sheared"]),
    ("Bracing", "frame", 10, ["Horizontal brace bent", "Diagonal brace disconnected"]),
    ("Beam", "beam", 22, ["Beam deflected under load", "Beam dented at front face", "Beam bent downward"]),
    ("Beam connector", "beam", 8, ["Connector tab cracked", "Connector deformed"]),
    ("Safety pin", "beam", 8, ["Safety lock missing", "Safety lock not engaged"]),
]
PRIORITY_W = [("Unload", 12), ("High", 18), ("Medium", 40), ("Low", 37)]
DUE_DAYS = {"Unload": 0, "High": 7, "Medium": 30, "Low": 90}
INSPECTORS = ["Inspector 1", "Inspector 2", "Inspector 3"]



def main():
    rng = random.Random(SEED)
    used, issues = set(), []
    while len(issues) < N_ISSUES:
        comp, kind, _, descs = rng.choices(COMPONENTS, weights=[c[2] for c in COMPONENTS])[0]
        row = rng.choices(ROWS, weights=[3, 5, 6, 4, 2, 2])[0]      # busy middle aisles get hit more
        if kind == "frame":
            loc = {"row": row, "frame": rng.randint(1, BAYS + 1)}
            key = (row, "f", loc["frame"], comp)
        else:
            lvl = rng.choices(range(1, LEVELS + 1), weights=[5, 3, 2, 1])[0]
            loc = {"row": row, "bay": rng.randint(1, BAYS), "level": lvl}
            key = (row, "b", loc["bay"], lvl, comp)
        if key in used:
            continue
        used.add(key)
        prio = rng.choices([p for p, _ in PRIORITY_W], weights=[w for _, w in PRIORITY_W])[0]
        if comp in ("Anchor", "Safety pin") and prio == "Unload":
            prio = "High"
        found = AS_OF - timedelta(days=rng.randint(0, 120))
        if prio == "Unload" and rng.random() < 0.5:
            found = AS_OF - timedelta(days=rng.randint(0, 2))     # fresh critical findings still open
        age = (AS_OF - found).days
        # older and more urgent issues are more likely already repaired
        p_fixed = min(0.9, age / 100 + (0.35 if prio in ("Unload", "High") else 0))
        status, repaired = "Open", None
        if (AS_OF - found).days > 2 and rng.random() < p_fixed:
            status = "Repaired"
            lag = {"Unload": 1, "High": 5, "Medium": 20, "Low": 45}[prio]
            repaired = min(AS_OF, found + timedelta(days=rng.randint(0, lag * 2)))
        elif rng.random() < 0.3:
            status = "Scheduled"
        issues.append({
            "loc": loc, "kind": kind, "component": comp, "priority": prio,
            "desc": rng.choice(descs), "status": status,
            "found": found.isoformat(), "due": (found + timedelta(days=DUE_DAYS[prio])).isoformat(),
            "repaired": repaired.isoformat() if repaired else None,
            "inspector": rng.choice(INSPECTORS),
        })
    issues.sort(key=lambda i: i["found"])
    for n, i in enumerate(issues, 1):
        i["id"] = f"RD-{n:04d}"
    data = {"meta": {"site": "Demo DC", "asOf": AS_OF.isoformat(), "rows": ROWS, "bays": BAYS,
                     "levels": LEVELS, "dueDays": DUE_DAYS}, "issues": issues}
    out = Path(__file__).resolve().parent.parent / "data"
    out.mkdir(exist_ok=True)
    (out / "sample.json").write_text(json.dumps(data, indent=1))
    from collections import Counter
    print(len(issues), Counter(i["priority"] for i in issues), Counter(i["status"] for i in issues))


if __name__ == "__main__":
    main()
