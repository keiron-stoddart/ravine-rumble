from pathlib import Path
from random import choice

from flask import Flask, render_template
from yfpy.query import YahooFantasySportsQuery


from configurations import CLIENT_ID, CLIENT_SECRET, PATH
from declarations import Team, RAVINE_RUMBLE, GAME_CODE, GAME_ID


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
