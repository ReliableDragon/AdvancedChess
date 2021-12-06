from collections import defaultdict
from ruleconverter import *
from game import Game

DEFAULT_RULES = {
    'en_passant': 'STANDARD',
    'starting_pieces': 'STANDARD',
    'move_set': 'STANDARD',
    'attack_set': 'STANDARD',
}

class Chess():
    games = defaultdict(lambda: {}, {
        "24601": {
            'width': 8,
            'height': 8,
            'pieces': [
                {'icon': 'white_pawn', 'type':'P', 'row': 0, 'col': 0, "valid_moves": [[0, 0]]},
                {'icon': 'black_pawn', 'type':'P', 'row': 0, 'col': 1, "valid_moves": [[0, 0]]},
                {'icon': 'white_queen', 'type':'Q', 'row': 1, 'col': 0, "valid_moves": [[0, 0]]},
                {'icon': 'black_queen', 'type':'Q', 'row': 1, 'col': 1, "valid_moves": [[0, 0]]},
                {'icon': 'white_king', 'type':'K', 'row': 7, 'col': 7, "valid_moves": [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]], "valid_attacks": [[0, 1]]},
                ],
            'rules': DEFAULT_RULES,
        },
    })

    rules = defaultdict(lambda: "STANDARD", {
        "TEST": """{
            "en_passant": "STANDARD",
            "starting_pieces": "XNX,XPX",
            "move_set": "STANDARD",
            "valid_attacks": "NONE",
            "attack_set": "STANDARD",
            "height": 5,
            "width": 3
        }""",
        "TEST2": """{
            "en_passant": "STANDARD",
            "starting_pieces": "XKX,QXX",
            "move_set": "STANDARD",
            "valid_attacks": "NONE",
            "attack_set": "STANDARD",
            "height": 5,
            "width": 3
        }""",
        "TEST3": """{
            "en_passant": "STANDARD",
            "starting_pieces": "RXXB,XBXX",
            "move_set": "STANDARD",
            "valid_attacks": "NONE",
            "attack_set": "STANDARD",
            "height": 5,
            "width": 4
        }""",
        "TEST4": """{
            "starting_pieces": "XXX,PPX",
            "height": 4,
            "width": 3
        }"""
    })

    def __init__(self):
        pass

    def get_state(self, game_id):
        print(f'Getting state for game id {game_id}')
        return self.games[game_id]

    def start_game(self, ruleset='STANDARD', named_ruleset=None):
        id, game = None, None
        if named_ruleset:
            print(f"Starting new game with named ruleset {named_ruleset}.")
            id, game = Game.new_game(self.rules[named_ruleset])
        else:
            id, game = Game.new_game(ruleset)
        self.games[id] = game
        return id
