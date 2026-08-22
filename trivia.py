import json
import threading
from datetime import datetime
from pathlib import Path

from declarations import TRIVIA_QUESTIONS, Team

DATA_FILE = Path(__file__).parent / "data" / "trivia.json"
_lock = threading.Lock()

# lobby -> question -> revealed -> (question -> revealed) ... -> finished
LOBBY = "lobby"
QUESTION = "question"
REVEALED = "revealed"
FINISHED = "finished"


def _blank_state() -> dict:
    return {"phase": LOBBY, "index": 0, "answers": {}, "updated_at": None}


def load_state() -> dict:
    if not DATA_FILE.exists():
        return _blank_state()
    with open(DATA_FILE) as f:
        state = json.load(f)
    # Tolerate a partially written or older file rather than 500-ing mid-game.
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


def record_answer(name: str, index: int, choice: int) -> tuple[bool, str]:
    """Answers are only accepted for the question that is currently open."""
    with _lock:
        state = load_state()
        if state["phase"] != QUESTION:
            return False, "That question is closed."
        if index != state["index"]:
            return False, "That question is no longer open."
        if not (0 <= choice < len(TRIVIA_QUESTIONS[index]["options"])):
            return False, "Invalid choice."

        state["answers"].setdefault(name, {})[str(index)] = choice
        _write(state)
    return True, ""


def advance(action: str) -> dict:
    with _lock:
        state = load_state()

        if action == "reset":
            state = _blank_state()
        elif action == "start":
            state.update({"phase": QUESTION, "index": 0})
        elif action == "reveal":
            if state["phase"] == QUESTION:
                state["phase"] = REVEALED
        elif action == "next":
            if state["index"] + 1 < len(TRIVIA_QUESTIONS):
                state.update({"phase": QUESTION, "index": state["index"] + 1})
            else:
                state["phase"] = FINISHED

        return _write(state)


def scores(state: dict | None = None) -> list[dict]:
    """Leaderboard, best first. Only counts questions that have been revealed."""
    state = state or load_state()
    answered_through = state["index"] if state["phase"] in (REVEALED, FINISHED) else state["index"] - 1

    board = []
    for name, given in state["answers"].items():
        correct = sum(
            1
            for i, q in enumerate(TRIVIA_QUESTIONS)
            if i <= answered_through and given.get(str(i)) == q["answer"]
        )
        board.append({"name": name, "score": correct, "answered": len(given)})

    board.sort(key=lambda r: (-r["score"], r["name"]))
    return board


def public_state(state: dict, name: str | None) -> dict:
    """
    The payload players poll for. The correct answer and its explanation are
    withheld until the host reveals, so they can't be read out of devtools.
    """
    phase, index = state["phase"], state["index"]
    payload = {
        "phase": phase,
        "index": index,
        "total": len(TRIVIA_QUESTIONS),
        "updated_at": state["updated_at"],
    }

    if phase in (QUESTION, REVEALED):
        question = TRIVIA_QUESTIONS[index]
        payload["question"] = {
            "text": question["question"],
            "options": question["options"],
        }
        payload["my_answer"] = state["answers"].get(name, {}).get(str(index))
        payload["answered_count"] = sum(
            1 for given in state["answers"].values() if str(index) in given
        )
        payload["player_count"] = len(Team)

        if phase == REVEALED:
            payload["correct"] = question["answer"]
            payload["note"] = question["note"]
            payload["tally"] = [
                sum(
                    1
                    for given in state["answers"].values()
                    if given.get(str(index)) == choice
                )
                for choice in range(len(question["options"]))
            ]

    if phase in (REVEALED, FINISHED):
        payload["scores"] = scores(state)

    return payload
