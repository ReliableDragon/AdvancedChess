from ruleconverter import *
import string
import json
import valid_moves
import coord
from invalid_move_error import InvalidMoveError

DEFAULT_RULES = {
    "en_passant": "STANDARD",
    "castling": "STANDARD",
    "starting_pieces": "STANDARD",
    "move_set": "STANDARD",
    "valid_attacks": "NONE",
    "attack_set": "STANDARD",
    "victory_condition": "STANDARD",
    "movement_modifiers": "STANDARD",
    "height": 8,
    "width": 8,
}

SWAP_TURN = {
    'white': 'black',
    'black': 'white',
}

# class Game():
#     def __init__(self, game_data):
#         self.width = game_data['width']
#         self.height = game_data['height']


def update_board(piece_data, rules):
    board = generate_board(piece_data, rules)
    piece_data = valid_moves.populate_valid_moves(piece_data, board, rules)
    populate_valid_attacks(piece_data, board, rules)

    return piece_data

# rules: dict/JSON (see example above)
# returns: (int, dict/JSON) (game ID, and dict containing all data about the game, to save in Firebase)
def new_game(rules):
    if rules == "STANDARD":
        rules = DEFAULT_RULES
    else:
        rules = json.loads(rules)
        for k, v in DEFAULT_RULES.items():
            if k not in rules.keys():
                rules[k] = v
    # JSON operations
    piece_ordering = get_piece_order(rules["starting_pieces"])
    pieces = generate_starting_pieces(piece_ordering, rules)
    # Python type operations
    pieces = update_board(pieces, rules)
    # board = generate_board(pieces, rules)
    # pieces = valid_moves.populate_valid_moves(pieces, board, rules)
    # populate_valid_attacks(pieces, board, rules)

    game_data = {
        "width": rules["width"],
        "height": rules["height"],
        "pieces": pieces,
        "rules": rules,
        "turn": "white",
        "winner": "",
    }
    return game_data

# game_data: dict/JSON{int: dict/JSON} (id to piece dict)
# move_data: dict/JSON
# returns: dict/JSON (updated game_data)
def make_move(game_data, move_data):
    # Extract salient data
    moving_piece_id = move_data['piece_id']
    moving_to = [move_data['row'], move_data['col']]
    piece_data = game_data['pieces']
    moving_piece = piece_data[moving_piece_id]
    valid_moves = moving_piece['valid_moves']

    if moving_piece['color'] != game_data['turn']:
        raise InvalidMoveError("Wrong color! It's not your turn!")

    if not moving_to in valid_moves:
        print(f"Attempted to move to {moving_to}, when valid spaces were {valid_moves}")
        raise InvalidMoveError("Invalid move!")

    # Will be empty if no captures
    captured_pieces = [id for id, piece in game_data['pieces'].items() if [piece['row'], piece['col']] == moving_to]
    for id in captured_pieces:
        moving_piece['captures'] += 1
        del piece_data[id]

    # Update piece's position
    moving_piece['row'] = move_data['row']
    moving_piece['col'] = move_data['col']
    moving_piece['moves'] += 1
    piece_data[moving_piece_id] = moving_piece

    # Update board and regenerate valid moves, then return it
    pieces = update_board(piece_data, game_data['rules'])
    game_data['pieces'] = pieces
    game_data['turn'] = SWAP_TURN[game_data['turn']]
    return game_data
