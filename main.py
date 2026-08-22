from pathlib import Path
from random import choice

from flask import Flask, render_template, request, jsonify
from yfpy.query import YahooFantasySportsQuery


from configurations import CLIENT_ID, CLIENT_SECRET, PATH
from declarations import (
    Team,
    RAVINE_RUMBLE,
    GAME_CODE,
    GAME_ID,
    Event,
    EVENT_LABELS,
    EVENT_DURATION_MINUTES,
    AVAILABILITY_ARCHIVED,
    SEASON_2026_EVENTS,
    LEAGUE_FINISHES,
    HISTORICAL_COMPARISON,
    SEASON_RESULTS,
    SEASON_RESULTS_YEARS,
    TRIVIA_QUESTIONS,
    STATS_HIDDEN,
)
from scheduling import (
    candidate_days,
    save_person_availability,
    get_person_availability,
    compute_results,
)
from prediction import predict_winner
import trivia


app = Flask(__name__)
GIFS = [
    'https://giphy.com/embed/vFhdC60CFCwgAUTQ6i',
    'https://giphy.com/embed/nEuNUZP8rX9YyDMVud',
    'https://giphy.com/embed/3ohc0Y2TA2KJRO66m4',
    'https://giphy.com/embed/l57gbvjm8xU5uVSDnx',
    'https://giphy.com/embed/3orieZBr6Oh8YmeR56',
    'https://giphy.com/embed/0Q2Idjtt38WLwrLGnO',
    'https://giphy.com/embed/jO1ZyDgmy9IBqFzPPm',
]


@app.context_processor
def nav_flags():
    """base.html is extended everywhere, so the nav's flags live here."""
    return {
        'stats_hidden': STATS_HIDDEN,
        'availability_archived': AVAILABILITY_ARCHIVED,
    }


def _win_probabilities(team_a, team_b):
    """Monte-Carlo win chance (whole %) for a live matchup, or (None, None).

    Returns None rather than a number whenever we can't compute a meaningful
    probability — the dev Yahoo token can be stale (scores fall back to
    unavailable.html) and projections are missing/zero before kickoff. In those
    cases the page renders without the probability instead of a bogus figure.
    """
    try:
        if not (team_a['team_projected_points'].total and team_b['team_projected_points'].total):
            return None, None
        a_prob, b_prob = predict_winner(team_a, team_b)
        return round(a_prob * 100), round(b_prob * 100)
    except Exception:
        app.logger.exception('Failed to compute win probability')
        return None, None


def _trivia_is_live():
    """Read-only peek so landing pages can nudge people toward a running game."""
    try:
        return trivia.load_state()['phase'] != trivia.LOBBY
    except Exception:
        app.logger.exception('Failed to read trivia state')
        return False


@app.route('/')
def home():
    # documentation: https://github.com/uberfastman/yfpy
    try:
        query = YahooFantasySportsQuery(
            league_id=RAVINE_RUMBLE,
            game_code=GAME_CODE,
            game_id=GAME_ID,
            yahoo_consumer_key=CLIENT_ID,
            yahoo_consumer_secret=CLIENT_SECRET,
            env_file_location=Path(PATH)
        )

        query.save_access_token_data_to_env_file(
            env_file_location=Path(PATH),
            save_json_to_var_only=True
        )

        paul = query.get_team_stats_by_week(Team.PAUL.value, 15)
        tim = query.get_team_stats_by_week(Team.TIM.value, 15)
    except Exception:
        app.logger.exception('Failed to fetch scores from Yahoo')
        return render_template(
            'unavailable.html', gif=choice(GIFS), trivia_live=_trivia_is_live()
        )

    tim_win, paul_win = _win_probabilities(tim, paul)
    return render_template(
        'losers.html',
        paul=paul, tim=tim, gif=choice(GIFS),
        tim_win=tim_win, paul_win=paul_win,
        trivia_live=_trivia_is_live(),
    )


@app.route('/bracket')
def bracket():
    return render_template('bracket.html')


@app.route('/2026')
def season_2026():
    return render_template('season_2026.html', events=SEASON_2026_EVENTS)


@app.route('/archives/2025')
def archive_2025():
    return render_template('archive_2025.html')


@app.route('/stats')
def stats():
    # Hiding the nav link alone wouldn't do much — the page answers every
    # trivia question, and the URL is already known.
    if STATS_HIDDEN:
        return render_template('stats_hidden.html'), 404

    return render_template(
        'stats.html',
        finishes=LEAGUE_FINISHES,
        historical=HISTORICAL_COMPARISON,
        season_results=SEASON_RESULTS,
        season_years=SEASON_RESULTS_YEARS,
    )


@app.route('/trivia')
def trivia_play():
    return render_template('trivia.html', team=Team)


@app.route('/trivia/state')
def trivia_state():
    name = request.args.get('name', '').upper()
    name = name if name in Team.__members__ else None
    return jsonify(trivia.public_state(trivia.load_state(), name))


@app.route('/trivia/answer', methods=['POST'])
def trivia_answer():
    payload = request.get_json(silent=True) or {}
    name = payload.get('name', '').upper()
    if name not in Team.__members__:
        return jsonify(ok=False, error='Unknown name'), 400

    try:
        index = int(payload.get('index'))
        choice = int(payload.get('choice'))
    except (TypeError, ValueError):
        return jsonify(ok=False, error='Invalid answer'), 400

    ok, error = trivia.record_answer(name, index, choice)
    return (jsonify(ok=True) if ok else (jsonify(ok=False, error=error), 409))


@app.route('/trivia/host')
def trivia_host():
    return render_template(
        'trivia_host.html',
        questions=TRIVIA_QUESTIONS,
        total=len(TRIVIA_QUESTIONS),
    )


@app.route('/trivia/host/state')
def trivia_host_state():
    """The host screen is the one place the answer is shown before the reveal."""
    state = trivia.load_state()
    payload = trivia.public_state(state, None)
    if state['phase'] in (trivia.QUESTION, trivia.REVEALED):
        payload['correct'] = TRIVIA_QUESTIONS[state['index']]['answer']
        payload['note'] = TRIVIA_QUESTIONS[state['index']]['note']
        payload['answered_by'] = sorted(
            name for name, given in state['answers'].items()
            if str(state['index']) in given
        )
    payload['scores'] = trivia.scores(state)
    return jsonify(payload)


@app.route('/trivia/host/action', methods=['POST'])
def trivia_host_action():
    action = (request.get_json(silent=True) or {}).get('action')
    if action not in ('start', 'reveal', 'next', 'reset'):
        return jsonify(ok=False, error='Unknown action'), 400
    trivia.advance(action)
    return jsonify(ok=True)


@app.route('/availability', methods=['GET'])
def availability():
    return render_template(
        'availability.html',
        team=Team,
        events=Event,
        labels=EVENT_LABELS,
        durations=EVENT_DURATION_MINUTES,
        days=candidate_days(),
        archived=AVAILABILITY_ARCHIVED,
    )


@app.route('/availability', methods=['POST'])
def availability_submit():
    if AVAILABILITY_ARCHIVED:
        return jsonify(ok=False, error='This poll is closed.'), 403

    payload = request.get_json(silent=True) or {}
    name = payload.get('name', '').upper()
    if name not in Team.__members__:
        return jsonify(ok=False, error='Unknown name'), 400

    slots = payload.get('slots', [])
    if not isinstance(slots, list):
        return jsonify(ok=False, error='Invalid slots'), 400

    updated_at = save_person_availability(name, slots)
    return jsonify(ok=True, updated_at=updated_at)


@app.route('/availability/mine')
def availability_mine():
    name = request.args.get('name', '').upper()
    if name not in Team.__members__:
        return jsonify(error='Unknown name'), 400
    slots = get_person_availability(name)
    return jsonify(submitted=slots is not None, slots=slots or [])


@app.route('/availability/results')
def availability_results():
    return render_template(
        'availability_results.html',
        events=Event,
        labels=EVENT_LABELS,
        durations=EVENT_DURATION_MINUTES,
        days=candidate_days(),
        results=compute_results(),
        total_people=len(Team),
        archived=AVAILABILITY_ARCHIVED,
    )
