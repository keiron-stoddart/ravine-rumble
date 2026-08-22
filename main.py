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
import pickem


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


def _yahoo_query():
    """Build the yfpy query exactly as home() does (same env-file token dance)."""
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
    return query


def _pickem_open_matchups(week):
    """Snapshot week `week`'s six matchups from Yahoo with probabilities frozen
    at open. Raises on any Yahoo failure — the host route turns that into a 502.

    yfpy is kept entirely out of pickem.py: this returns the plain dict list
    that pickem.advance('open', ...) stores verbatim.
    """
    query = _yahoo_query()
    raw = query.get_league_matchups_by_week(week)
    id_to_name = {m.value: m.name for m in Team}
    matchups = []
    for i, mu in enumerate(raw, start=1):
        home_t, away_t = mu.teams[0], mu.teams[1]
        home_dict = {
            'team_points': home_t.team_points,
            'team_projected_points': home_t.team_projected_points,
        }
        away_dict = {
            'team_points': away_t.team_points,
            'team_projected_points': away_t.team_projected_points,
        }
        home_prob, away_prob = predict_winner(home_dict, away_dict)
        matchups.append({
            'id': f'{week}-{i}',
            'home': id_to_name.get(home_t.team_id),
            'away': id_to_name.get(away_t.team_id),
            'home_proj': round(home_t.team_projected_points.total, 1),
            'away_proj': round(away_t.team_projected_points.total, 1),
            'home_prob': round(home_prob, 2),
            'away_prob': round(away_prob, 2),
            'winner': None,
        })
    return matchups


def _pickem_score_winners(week, stored_matchups):
    """Re-fetch week `week` from Yahoo and resolve each stored matchup's winner
    (a Team name or "TIE"). Matched by team-name pair, not Yahoo ordering, so a
    reordered response can't misattribute a result. Raises on Yahoo failure.
    """
    query = _yahoo_query()
    raw = query.get_league_matchups_by_week(week)
    id_to_name = {m.value: m.name for m in Team}
    by_pair = {}
    for mu in raw:
        home_t, away_t = mu.teams[0], mu.teams[1]
        home_name = id_to_name.get(home_t.team_id)
        away_name = id_to_name.get(away_t.team_id)
        hp = home_t.team_points.total
        ap = away_t.team_points.total
        if getattr(mu, 'is_tied', 0) or hp == ap:
            winner = 'TIE'
        else:
            winner = home_name if hp > ap else away_name
        by_pair[frozenset((home_name, away_name))] = winner
    winners = {}
    for m in stored_matchups:
        winner = by_pair.get(frozenset((m['home'], m['away'])))
        if winner is not None:
            winners[m['id']] = winner
    return winners


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


@app.route('/pickem')
def pickem_play():
    return render_template('pickem.html', team=Team)


@app.route('/pickem/state')
def pickem_state():
    name = request.args.get('name', '').upper()
    name = name if name in Team.__members__ else None
    return jsonify(pickem.public_state(pickem.load_state(), name))


@app.route('/pickem/pick', methods=['POST'])
def pickem_pick():
    payload = request.get_json(silent=True) or {}
    name = payload.get('name', '').upper()
    if name not in Team.__members__:
        return jsonify(ok=False, error='Unknown name'), 400

    week = payload.get('week')
    if week is None:
        return jsonify(ok=False, error='Missing week'), 400

    # Accept either a single {matchup_id, pick} tap or a whole {picks: {...}} card.
    if 'picks' in payload and isinstance(payload['picks'], dict):
        ok, error = pickem.record_picks(name, week, payload['picks'])
    else:
        matchup_id = payload.get('matchup_id')
        pick = (payload.get('pick') or '').upper()
        if not matchup_id or pick not in Team.__members__:
            return jsonify(ok=False, error='Invalid pick'), 400
        ok, error = pickem.record_pick(name, week, matchup_id, pick)

    return jsonify(ok=True) if ok else (jsonify(ok=False, error=error), 409)


@app.route('/pickem/host')
def pickem_host():
    return render_template('pickem_host.html')


@app.route('/pickem/host/state')
def pickem_host_state():
    """Like /pickem/state but includes winners before the reveal (host-only)."""
    state = pickem.load_state()
    payload = pickem.public_state(state, None)
    week = state['current_week']
    wk = state['weeks'].get(str(week)) if week is not None else None
    if wk:
        payload['stored_status'] = wk.get('status')
        payload['matchups'] = [dict(m) for m in wk['matchups']]  # winners visible to host
        payload['pickers'] = sorted(state['picks'].get(str(week), {}).keys())
    return jsonify(payload)


@app.route('/pickem/host/action', methods=['POST'])
def pickem_host_action():
    payload = request.get_json(silent=True) or {}
    action = payload.get('action')
    if action not in ('open', 'lock', 'score', 'reset'):
        return jsonify(ok=False, error='Unknown action'), 400

    try:
        week = int(payload.get('week'))
    except (TypeError, ValueError):
        return jsonify(ok=False, error='Invalid week'), 400

    if action == 'open':
        try:
            matchups = _pickem_open_matchups(week)
        except Exception:
            app.logger.exception('Failed to fetch matchups from Yahoo')
            return jsonify(ok=False, error='Could not reach Yahoo'), 502
        locks_at = (payload.get('locks_at') or '').strip() or None
        pickem.advance('open', week, matchups=matchups, locks_at=locks_at)
    elif action == 'score':
        stored = pickem.load_state()['weeks'].get(str(week), {}).get('matchups', [])
        try:
            winners = _pickem_score_winners(week, stored)
        except Exception:
            app.logger.exception('Failed to fetch final scores from Yahoo')
            return jsonify(ok=False, error='Could not reach Yahoo'), 502
        pickem.advance('score', week, winners=winners)
    else:
        pickem.advance(action, week)

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
