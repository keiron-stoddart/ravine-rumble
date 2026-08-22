import json
import threading
from datetime import datetime
from pathlib import Path

from declarations import Team

DATA_FILE = Path(__file__).parent / "data" / "pickem.json"
_lock = threading.Lock()

# upcoming -> open -> locked -> scored  (per week; reset drops one week)
UPCOMING = "upcoming"
OPEN = "open"
LOCKED = "locked"
SCORED = "scored"


def _blank_state() -> dict:
    return {"season": 2026, "current_week": None, "weeks": {}, "picks": {}, "updated_at": None}


def load_state() -> dict:
    if not DATA_FILE.exists():
        return _blank_state()
    with open(DATA_FILE) as f:
        state = json.load(f)
    # Tolerate a partially written or older file rather than 500-ing mid-week.
    base = _blank_state()
    base.update({k: v for k, v in state.items() if k in base})
    return base


def _write(state: dict) -> dict:
    state["updated_at"] = datetime.now().isoformat(timespec="seconds")
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = DATA_FILE.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
    tmp.replace(DATA_FILE)
    return state


def _effective_status(wk: dict) -> str:
    """A week that is still `open` but past its `locks_at` reads as locked, so
    kickoff freezes picks even if the host never clicked Lock."""
    status = wk.get("status")
    if status == OPEN and wk.get("locks_at"):
        try:
            if datetime.now() >= datetime.fromisoformat(wk["locks_at"]):
                return LOCKED
        except (ValueError, TypeError):
            pass
    return status


def advance(action: str, week, matchups=None, winners=None, locks_at=None) -> dict:
    """Host-owned week lifecycle. main.py supplies `matchups`/`winners` after
    its own Yahoo fetch — this module never touches the network."""
    week = str(week)
    with _lock:
        state = load_state()
        wk = state["weeks"].get(week)

        if action == "open":
            if wk and wk.get("status") == SCORED:
                return state  # refuse to re-open a scored week
            state["weeks"][week] = {
                "status": OPEN,
                "locks_at": locks_at,
                "matchups": matchups or [],
                "updated_at": datetime.now().isoformat(timespec="seconds"),
            }
            state["current_week"] = int(week) if week.isdigit() else week
        elif action == "lock":
            if wk and wk.get("status") == OPEN:
                wk["status"] = LOCKED
        elif action == "score":
            if wk:
                by_id = winners or {}
                for m in wk["matchups"]:
                    if m["id"] in by_id:
                        m["winner"] = by_id[m["id"]]
                wk["status"] = SCORED
        elif action == "reset":
            # Targeted: drop just this week so prior weeks' leaderboard survives.
            state["weeks"].pop(week, None)
            state["picks"].pop(week, None)
            if str(state.get("current_week")) == week:
                remaining = sorted((int(w) for w in state["weeks"] if w.isdigit()), reverse=True)
                state["current_week"] = remaining[0] if remaining else None

        return _write(state)


def record_pick(name: str, week, matchup_id: str, pick: str) -> tuple[bool, str]:
    with _lock:
        state = load_state()
        wk = state["weeks"].get(str(week))
        if not wk:
            return False, "That week isn't open."
        if _effective_status(wk) != OPEN:
            return False, "Picks are locked for this week."
        m = next((m for m in wk["matchups"] if m["id"] == matchup_id), None)
        if m is None:
            return False, "Unknown matchup."
        if pick not in (m["home"], m["away"]):
            return False, "Pick must be one of the two teams."
        rec = state["picks"].setdefault(str(week), {}).setdefault(
            name, {"picks": {}, "updated_at": None}
        )
        rec["picks"][matchup_id] = pick
        rec["updated_at"] = datetime.now().isoformat(timespec="seconds")
        _write(state)
    return True, ""


def record_picks(name: str, week, picks: dict) -> tuple[bool, str]:
    """Whole-card upsert. All picks must be valid or nothing is written."""
    with _lock:
        state = load_state()
        wk = state["weeks"].get(str(week))
        if not wk:
            return False, "That week isn't open."
        if _effective_status(wk) != OPEN:
            return False, "Picks are locked for this week."
        valid = {m["id"]: (m["home"], m["away"]) for m in wk["matchups"]}
        cleaned = {}
        for mid, pick in (picks or {}).items():
            if mid not in valid:
                return False, "Unknown matchup."
            if pick not in valid[mid]:
                return False, "Pick must be one of the two teams."
            cleaned[mid] = pick
        rec = state["picks"].setdefault(str(week), {}).setdefault(
            name, {"picks": {}, "updated_at": None}
        )
        rec["picks"].update(cleaned)
        rec["updated_at"] = datetime.now().isoformat(timespec="seconds")
        _write(state)
    return True, ""


def week_score(state: dict, week) -> list[dict]:
    """Upset-weighted points for one week; only meaningful once SCORED.

    A correct pick scores round(100 * (1 - prob-of-picked-team)) with the
    probability frozen at open, so calling an underdog is worth more than
    riding a favorite. A tied game (winner == "TIE") counts either pick as
    right. Voided/unscored games (winner is None) contribute nothing.
    """
    wk = state["weeks"].get(str(week))
    if not wk:
        return []
    info = {
        m["id"]: {
            "home": (m["home"], m["home_prob"]),
            "away": (m["away"], m["away_prob"]),
            "winner": m.get("winner"),
        }
        for m in wk["matchups"]
    }
    rows = []
    for name, rec in state["picks"].get(str(week), {}).items():
        pts, correct = 0, 0
        for mid, picked in rec["picks"].items():
            m = info.get(mid)
            if not m or m["winner"] is None:
                continue
            if picked == m["home"][0]:
                p = m["home"][1]
            elif picked == m["away"][0]:
                p = m["away"][1]
            else:
                continue
            if picked == m["winner"] or m["winner"] == "TIE":
                pts += round(100 * (1 - p))
                correct += 1
        rows.append({"name": name, "points": pts, "correct": correct})
    rows.sort(key=lambda r: (-r["points"], r["name"]))
    return rows


def leaderboard(state: dict) -> list[dict]:
    """Season totals across every SCORED week, best first."""
    totals: dict[str, dict] = {}
    for week, wk in state["weeks"].items():
        if wk.get("status") != SCORED:
            continue
        for row in week_score(state, week):
            t = totals.setdefault(
                row["name"], {"name": row["name"], "points": 0, "correct": 0, "weeks": 0}
            )
            t["points"] += row["points"]
            t["correct"] += row["correct"]
            t["weeks"] += 1
    return sorted(totals.values(), key=lambda r: (-r["points"], r["name"]))


def public_state(state: dict, name: str | None) -> dict:
    """What the player poller receives. `winner` is withheld until the week is
    scored so it can't be read out of devtools before games resolve."""
    week = state["current_week"]
    wk = state["weeks"].get(str(week)) if week is not None else None
    payload = {
        "week": week,
        "updated_at": state["updated_at"],
        "leaderboard": leaderboard(state),
    }
    if wk:
        payload["status"] = _effective_status(wk)
        payload["locks_at"] = wk.get("locks_at")
        payload["matchups"] = [
            {k: m[k] for k in ("id", "home", "away", "home_prob", "away_prob", "home_proj", "away_proj")}
            | ({"winner": m.get("winner")} if wk.get("status") == SCORED else {})
            for m in wk["matchups"]
        ]
        payload["my_picks"] = (
            state["picks"].get(str(week), {}).get(name, {}).get("picks", {}) if name else {}
        )
        payload["picker_count"] = len(state["picks"].get(str(week), {}))
        payload["player_count"] = len(Team)
        if wk.get("status") == SCORED:
            payload["week_score"] = week_score(state, week)
    return payload
