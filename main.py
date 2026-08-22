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
)
from scheduling import (
    candidate_days,
    save_person_availability,
    get_person_availability,
    compute_results,
)


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
        return render_template('unavailable.html', gif=choice(GIFS))

    return render_template(
        'losers.html',
        paul=paul, tim=tim, gif=choice(GIFS)
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
    return render_template(
        'stats.html',
        finishes=LEAGUE_FINISHES,
        historical=HISTORICAL_COMPARISON,
        season_results=SEASON_RESULTS,
        season_years=SEASON_RESULTS_YEARS,
    )


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
