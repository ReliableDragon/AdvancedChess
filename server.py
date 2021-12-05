from chess import Chess
from flask import Flask, render_template
import json

app = Flask(__name__)
chess = Chess()

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route("/play/")
@app.route("/play/<string:game_id>")
def play_game(game_id=None):
    if game_id == "24601":
        return render_template('game.html', game_id=game_id)
    else:
        return render_template('bad_game.html', game_id=game_id)

@app.route("/state/<string:game_id>")
def get_game_state(game_id=None):
    state = chess.get_state(game_id)
    response = json.dumps(state)
    return response
