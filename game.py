from ruleconverter import *
import random
import string
import json
import valid_moves

DEFAULT_RULES = {
    "en_passant": "STANDARD",
    "castling": "STANDARD",
    "starting_pieces": "STANDARD",
    "move_set": "STANDARD",
    "valid_attacks": "NONE",
    "attack_set": "STANDARD",
    "height": 8,
    "width": 8,
}

class Game():

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
        id = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        # Python type operations
        board = generate_board(pieces, rules)
        pieces = valid_moves.populate_valid_moves(pieces, board, rules)
        populate_valid_attacks(pieces, board, rules)

        game_data = {
            "width": rules["width"],
            "height": rules["height"],
            "pieces": pieces,
            "rules": rules,
            "turn": "white",
        }
        return id, game_data
