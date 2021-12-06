from chess import Chess
from flask import Flask, render_template, redirect, request
import json
from invalid_move_error import InvalidMoveError

app = Flask(__name__)
chess = Chess()

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route("/join/")
@app.route("/join/<string:game_id>")
def join_game(game_id=None):
    if game_id == "24601":
        return render_template('game.html', game_id=game_id)
    else:
        return render_template('bad_game.html', game_id=game_id)

@app.route("/state/<string:game_id>")
def get_game_state(game_id=None):
    state = chess.get_state(game_id)
    response = json.dumps(state)
    return response

@app.route("/setup/")
def setup_game(ruleset=None):
    return render_template('setup.html')

@app.route("/start/", methods=['POST'])
def start_game(ruleset=None):
    # We accept non-JSON responses in case the rules are "STANDARD".
    rules = request.get_data()
    game_id = chess.start_game(rules)
    return json.dumps({'game_id': game_id}), 200

@app.route("/start_demo/")
@app.route("/start_demo/<string:ruleset>")
def start_demo_game(ruleset=None):
    if ruleset == None:
        return render_template('bad_game.html', game_id=game_id)
    game_id = chess.start_game(named_ruleset=ruleset)
    # Temporary hack while we're abusing the game ID box for rulesets
    # Remove start method and merge with play once rulepicker is in place.
    return redirect(f'/play/{game_id}')

@app.route("/play/")
@app.route("/play/<string:game_id>")
def play_game(game_id=None):
    if game_id:
        return render_template('game.html', game_id=game_id)
    else:
        return render_template('bad_game.html', game_id=game_id)

@app.route("/move/", methods=['POST'])
def make_move():
    if not request.is_json:
        print(f"Got bad json: {request.get_data()}")
        return f"Unable to parse move: {request.get_data()}", 400
    data = request.get_json()
    try:
        response = chess.make_move(data['game_id'], data['move_data'])
    except InvalidMoveError as e:
        print("Invalid move!")
        return f"Invalid move: {str(e)}", 400
    return json.dumps(response)
