"""GroupMe bot: a post helper plus replies to !commands sent in the group chat.

GroupMe POSTs every group message to the bot's callback URL (/groupme/callback);
`reply_to` turns one of those payloads into the text to answer with (or None).
The bot ID is GROUPME_BOT_ID, from the environment or the gitignored .env file
next to this module — unset, `post` is a silent no-op.
"""
import json
import logging
import os
import urllib.request
from pathlib import Path

from dotenv import dotenv_values

import pickem
from declarations import Team
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
    return "Commands: !pickem (standings), !power (power rankings), !help"


COMMANDS = {
    "!help": _help_text,
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
