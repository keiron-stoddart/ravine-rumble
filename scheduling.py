import json
import threading
from datetime import date, datetime, timedelta
from pathlib import Path

from declarations import (
    POLL_START_DATE,
    POLL_END_DATE,
    DAY_BLOCKS,
    WEEKDAY_BLOCKS,
    WEEKEND_BLOCKS,
    Team,
)

DATA_FILE = Path(__file__).parent / "data" / "availability.json"
_lock = threading.Lock()


def applicable_blocks(d: date) -> list[str]:
    return WEEKEND_BLOCKS if d.weekday() >= 5 else WEEKDAY_BLOCKS


def generate_candidate_slots() -> list[tuple[date, str]]:
    slots = []
    d = POLL_START_DATE
    while d <= POLL_END_DATE:
        for block in applicable_blocks(d):
            slots.append((d, block))
        d += timedelta(days=1)
    return slots


def slot_id(d: date, block: str) -> str:
    return f"{d.isoformat()}:{block}"


def candidate_days() -> list[dict]:
    """Candidate slots grouped by date, for grid rendering (rows = dates)."""
    days = []
    d = POLL_START_DATE
    while d <= POLL_END_DATE:
        applicable = applicable_blocks(d)
        days.append({
            "date": d,
            "label": d.strftime("%a %b %-d"),
            "blocks": [
                {
                    "name": b,
                    "slot": slot_id(d, b) if b in applicable else None,
                    "applicable": b in applicable,
                }
                for b in DAY_BLOCKS
            ],
        })
        d += timedelta(days=1)
    return days


def valid_slot_ids() -> set[str]:
    return {slot_id(d, block) for d, block in generate_candidate_slots()}


def load_availability() -> dict:
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE) as f:
        return json.load(f)


def save_person_availability(name: str, slot_ids: list[str]) -> str:
    valid = valid_slot_ids()
    cleaned = sorted(s for s in slot_ids if s in valid)
    updated_at = datetime.now().isoformat(timespec="seconds")
    with _lock:
        data = load_availability()
        data[name] = {"slots": cleaned, "updated_at": updated_at}
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = DATA_FILE.with_suffix(".tmp")
        with open(tmp, "w") as f:
            json.dump(data, f, indent=2)
        tmp.replace(DATA_FILE)
    return updated_at


def get_person_availability(name: str) -> list[str] | None:
    """None means the person has never submitted; [] means they submitted with nothing available."""
    record = load_availability().get(name)
    return None if record is None else record.get("slots", [])


def compute_results() -> dict:
    people = load_availability()

    heatmap: dict[str, dict] = {s: {"count": 0, "names": []} for s in valid_slot_ids()}
    for name, record in people.items():
        for s in record.get("slots", []):
            if s in heatmap:
                heatmap[s]["count"] += 1
                heatmap[s]["names"].append(name)

    best_count = max((v["count"] for v in heatmap.values()), default=0)
    best = (
        sorted(s for s, v in heatmap.items() if v["count"] == best_count)
        if best_count > 0
        else []
    )

    submitted = sorted(people.keys())
    missing = sorted(m.name for m in Team if m.name not in people)

    return {
        "heatmap": heatmap,
        "best": best,
        "best_count": best_count,
        "submitted": submitted,
        "missing": missing,
    }
