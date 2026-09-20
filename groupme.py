"""GroupMe bot: a post helper plus replies to !commands sent in the group chat.

GroupMe POSTs every group message to the bot's callback URL (/groupme/callback);
`reply_to` turns one of those payloads into the text to answer with (or None).
The bot ID is GROUPME_BOT_ID, from the environment or the gitignored .env file
next to this module — unset, `post` is a silent no-op.
"""
import json
import logging
import os
import random
import urllib.request
from pathlib import Path

from dotenv import dotenv_values

import pickem
from declarations import HISTORICAL_COMPARISON, SEASON_RESULTS, Team
from power_rankings import POWER_RANKINGS

POST_URL = "https://api.groupme.com/v3/bots/post"
MAX_LEN = 1000  # GroupMe's per-message cap
SITE = "https://ravinerumble.com"
ENV_FILE = Path(__file__).parent / ".env"

log = logging.getLogger(__name__)


def _bot_id() -> str | None:
    # Read per call so a new .env takes effect without restarting the server.
    return os.environ.get("GROUPME_BOT_ID") or dotenv_values(ENV_FILE).get("GROUPME_BOT_ID")


def post(text: str) -> bool:
    """Send `text` to the group as the bot. Never raises; returns whether it sent."""
    bot_id = _bot_id()
    if not bot_id:
        log.warning("GROUPME_BOT_ID is not set; not posting")
        return False
    body = json.dumps({"bot_id": bot_id, "text": text[:MAX_LEN]}).encode()
    req = urllib.request.Request(
        POST_URL, data=body, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5):
            return True
    except Exception:
        log.exception("Failed to post to GroupMe")
        return False


def _pickem_text() -> str:
    state = pickem.load_state()
    lines = []

    week = state["current_week"]
    wk = state["weeks"].get(str(week)) if week is not None else None
    if wk and pickem._effective_status(wk) == pickem.OPEN:
        picked = len(state["picks"].get(str(week), {}))
        lines.append(f"Week {week} pick'em is open ({picked}/{len(Team)} have picked): {SITE}/pickem")

    board = pickem.leaderboard(state)
    if board:
        lines.append("Pick'em standings:")
        lines += [
            f"{i}. {row['name'].title()} — {row['points']} pts"
            for i, row in enumerate(board, start=1)
        ]
    elif not lines:
        lines.append("No pick'em weeks have been scored yet.")
    return "\n".join(lines)


def _power_text() -> str:
    teams = POWER_RANKINGS["teams"]
    latest = max(e["week"] for t in teams for e in t["entries"])
    ranked = sorted(
        (e["rank"], t["manager"], e.get("team") or t["team"])
        for t in teams
        for e in t["entries"]
        if e["week"] == latest
    )
    lines = [f"Week {latest} power rankings:"]
    lines += [f"{rank}. {manager} — {team}" for rank, manager, team in ranked]
    lines.append(f"{SITE}/2026/power-rankings")
    return "\n".join(lines)


def _help_text() -> str:
    return "My sole purpose is to clown on Tyler."


# Each clown fact is computed from the site's data, so it stays true as it
# updates, and returns None when it wouldn't actually be embarrassing.
def _tyler_seasons() -> list[dict]:
    return sorted((s for s in SEASON_RESULTS if s["manager"] == "Tyler"), key=lambda s: s["year"])


def _clown_power() -> str | None:
    entries = sorted(
        next(t for t in POWER_RANKINGS["teams"] if t["manager"] == "Tyler")["entries"],
        key=lambda e: e["week"],
    )
    latest = entries[-1]
    if latest["rank"] <= 6:
        return None
    text = f"Tyler is #{latest['rank']} of {len(POWER_RANKINGS['teams'])} in the week {latest['week']} power rankings"
    if len(entries) > 1 and entries[-2]["rank"] < latest["rank"]:
        text += f", down from #{entries[-2]['rank']}"
    return text + "."


def _clown_last_place() -> str | None:
    teams_per_year = {}
    for s in SEASON_RESULTS:
        teams_per_year[s["year"]] = max(teams_per_year.get(s["year"], 0), s["finish"])
    years = [s["year"] for s in _tyler_seasons() if s["finish"] == teams_per_year[s["year"]]]
    if len(years) < 2:
        return None
    return f"Tyler has finished dead last in the league {len(years)} times ({', '.join(map(str, years))})."


def _clown_worst_season() -> str:
    worst = min(_tyler_seasons(), key=lambda s: s["point_diff"])
    return (
        f"In {worst['year']} Tyler went {worst['wins']}-{worst['losses']} with a "
        f"{worst['point_diff']:+.0f} point differential. Team name: {worst['team']}."
    )


def _clown_team_names() -> str:
    seasons = _tyler_seasons()
    n = sum("keiron" in s["team"].lower() for s in seasons)
    return f"Tyler has named the team after Keiron in {n} of {len(seasons)} seasons."


def _clown_avg_finish() -> str | None:
    rows = sorted(HISTORICAL_COMPARISON, key=lambda r: r["finish"])
    me = next(r for r in rows if r["manager"] == "Tyler")
    rank = rows.index(me) + 1
    if rank <= len(rows) // 2:
        return None
    text = f"Tyler ranks #{rank} of {len(rows)} in average finish over {me['seasons']} seasons ({me['finish']})."
    worse = [r["manager"] for r in rows if r["finish"] > me["finish"]]
    if len(worse) == 1:
        text += f" Only {worse[0]} is worse."
    return text


CLOWN_FACTS = [_clown_power, _clown_last_place, _clown_worst_season, _clown_team_names, _clown_avg_finish]


def _clown_text() -> str:
    facts = [f for f in (fact() for fact in CLOWN_FACTS) if f]
    return "🤡 " + (random.choice(facts) if facts else "Nothing embarrassing on Tyler right now. Suspicious.")


COMMANDS = {
    "!help": _help_text,
    "!clown": _clown_text,
    "!pickem": _pickem_text,
    "!power": _power_text,
}


def reply_to(message: dict) -> str | None:
    """Text to answer a GroupMe callback payload with, or None to stay quiet."""
    # Ignore bots (ours included), or the bot would answer its own replies forever.
    if message.get("sender_type") != "user":
        return None
    parts = (message.get("text") or "").strip().lower().split()
    handler = COMMANDS.get(parts[0]) if parts else None
    return handler() if handler else None
