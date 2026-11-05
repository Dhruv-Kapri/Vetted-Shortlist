"""Summarise the 140 by-hand checks per area, random and suspicious halves kept apart.

Inputs: research/hand_sample.json (what the pages show), research/hand_eye.json ({id: {"photos": category,
"note": str}} from looking at the contact sheets), research/hand_permits.json ({id: {"permit_price": int}}).
Photo categories: ok, cant_place, views_only, reused_other_units, staged_undisclosed, staged_disclosed,
other_building, duplicate.
"""

import json
from collections import defaultdict
from pathlib import Path

PROBLEM_PHOTOS: set[str] = {"views_only", "reused_other_units", "staged_undisclosed", "other_building", "duplicate"}
NAMES: dict[str, str] = {
    "palm-jumeirah": "Palm Jumeirah", "downtown-dubai": "Downtown Dubai", "dubai-marina": "Dubai Marina",
    "jumeirah-village-circle": "JVC", "discovery-gardens": "Discovery Gardens",
    "international-city": "International City", "binghatti-heights": "Binghatti Heights (JVC tower)",
}


def main() -> None:
    sample: list[dict] = json.loads(Path("research/hand_sample.json").read_text())
    eye: dict[str, dict] = json.loads(Path("research/hand_eye.json").read_text())
    permits_path = Path("research/hand_permits.json")
    permits: dict[str, dict] = json.loads(permits_path.read_text()) if permits_path.exists() else {}
    agg: dict[tuple[str, str], dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for r in sample:
        a = agg[(r["area"], r["why"])]
        a["n"] += 1
        a["bait"] += r["vs_deals"] is not None and r["vs_deals"] < -0.25
        a["stale"] += r["stale_days"] > 45
        e = eye.get(r["id"], {})
        a["eye_checked"] += bool(e)
        a["photo_problem"] += e.get("photos") in PROBLEM_PHOTOS
        a["staged"] += e.get("photos") in {"staged_undisclosed", "staged_disclosed"}
        pm = permits.get(r["id"])
        if pm:
            a["permit_checked"] += 1
            a["permit_mismatch"] += pm.get("permit_price") != r["price"]  # includes "no permit shown"
        a["any_sign"] += bool((r["vs_deals"] is not None and r["vs_deals"] < -0.10) or r["stale_days"] > 45
                              or e.get("photos") in PROBLEM_PHOTOS or (pm and pm.get("permit_price") != r["price"]))
    print("| Area | Sample | n | Bait (<75%) | Stale >45 d | Photo problem | Staged | Permit checked / price differs | Any sign |")
    print("|---|---|---|---|---|---|---|---|---|")
    for (area, why), a in sorted(agg.items(), key=lambda kv: (list(NAMES).index(kv[0][0]), kv[0][1])):
        print(f"| {NAMES[area]} | {why} | {a['n']} | {a['bait']} | {a['stale']} | {a['photo_problem']} | {a['staged']} "
              f"| {a['permit_checked']} / {a['permit_mismatch']} | {a['any_sign']} |")
    tot: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for (_, why), a in agg.items():
        for k, v in a.items():
            tot[why][k] += v
    for why, a in tot.items():
        print(f"| **All** | {why} | {a['n']} | {a['bait']} | {a['stale']} | {a['photo_problem']} | {a['staged']} "
              f"| {a['permit_checked']} / {a['permit_mismatch']} | {a['any_sign']} |")


if __name__ == "__main__":
    main()
