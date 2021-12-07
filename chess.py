from collections import defaultdict
from game import Game
import random
import string
import copy
import pprint

DEFAULT_RULES = {
    'en_passant': 'STANDARD',
    'starting_pieces': 'STANDARD',
    'move_set': 'STANDARD',
    'attack_set': 'NONE',
}

class Chess():
    games = defaultdict(lambda: {}, {
        "24601": {
            'width': 8,
            'height': 8,
            'pieces': [
                {'icon': 'white_pawn', 'type': 'P', 'row': 0,
                 'col': 0, "valid_moves": [[0, 0]]},
                {'icon': 'black_pawn', 'type': 'P', 'row': 0,
                 'col': 1, "valid_moves": [[0, 0]]},
                {'icon': 'white_queen', 'type': 'Q', 'row': 1,
                 'col': 0, "valid_moves": [[0, 0]]},
                {'icon': 'black_queen', 'type': 'Q', 'row': 1,
                 'col': 1, "valid_moves": [[0, 0]]},
                {'icon': 'white_king', 'type': 'K', 'row': 7, 'col': 7, "valid_moves": [[0, 0], [
                    1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]], "valid_attacks": [[0, 1]]},
            ],
            'rules': DEFAULT_RULES,
        },
        "24602": {
            'width': 2,
            'height': 4,
            'pieces': {
                'black_R_00': {
                    'id': 'black_R_00',
                    'icon': 'black_rook',
                    'type': 'R',
                    'color': 'black',
                    'row': 0,
                    'col': 0,
                    'valid_moves': [],
                    'valid_attacks': None,
                    'special': None,
                    'moves': 0,
                    'captures': 0
                },
                'black_N_01': {
                    'id': 'black_N_01',
                    'icon': 'black_knight',
                    'type': 'N',
                    'color': 'black',
                    'row': 0,
                    'col': 1,
                    'valid_moves': [[2, 0], [2, 0]],
                    'valid_attacks': None,
                    'special': None,
                    'moves': 0,
                    'captures': 0
                },
                'black_P_10': {
                    'id': 'black_P_10',
                    'icon': 'black_pawn',
                    'type': 'P',
                    'color': 'black',
                    'row': 1,
                    'col': 0,
                    'valid_moves': [[2, 1]],
                    'valid_attacks': None,
                    'special': None,
                    'moves': 0,
                    'captures': 0
                },
                'black_P_11': {
                    'id': 'black_P_11',
                    'icon': 'black_pawn',
                    'type': 'P',
                    'color': 'black',
                    'row': 1,
                    'col': 1,
                    'valid_moves': [[2, 0]],
                    'valid_attacks': None,
                    'special': None,
                    'moves': 0,
                    'captures': 0
                },
                'white_R_30': {
                    'id': 'white_R_30',
                    'icon': 'white_rook',
                    'type': 'R',
                    'color': 'white',
                    'row': 3,
                    'col': 0,
                    'valid_moves': [],
                    'valid_attacks': None,
                    'special': None,
                    'moves': 0,
                    'captures': 0
                },
                'white_N_31': {
                    'id': 'white_N_31',
                    'icon': 'white_knight',
                    'type': 'N',
                    'color': 'white',
                    'row': 3,
                    'col': 1,
                    'valid_moves': [[1, 0], [1, 0]],
                    'valid_attacks': None,
                    'special': None,
                    'moves': 0,
                    'captures': 0
                },
                'white_P_20': {
                    'id': 'white_P_20',
                    'icon': 'white_pawn',
                    'type': 'P',
                    'color': 'white',
                    'row': 2,
                    'col': 0,
                    'valid_moves': [[1, 1]],
                    'valid_attacks': None,
                    'special': None,
                    'moves': 0,
                    'captures': 0
                },
                'white_P_21': {
                    'id': 'white_P_21',
                    'icon': 'white_pawn',
                    'type': 'P',
                    'color': 'white',
                    'row': 2,
                    'col': 1,
                    'valid_moves': [[1, 0]],
                    'valid_attacks': None,
                    'special': None,
                    'moves': 0,
                    'captures': 0
                }
            },
            'rules': {
                'en_passant': 'STANDARD',
                'starting_pieces': 'STANDARD',
                'height': 4,
                'width': 2,
                'castling': 'STANDARD',
                'move_set': 'STANDARD',
                'attack_set': 'NONE',
            },
            'turn': 'white',
            "winner": "",
        }
    })



    rules = defaultdict(lambda: "STANDARD", {
        "TEST": """{
            "en_passant": "STANDARD",
            "starting_pieces": "XNX,XPX",
            "move_set": "STANDARD",
            "attack_set": "NONE",
            "height": 5,
            "width": 3
        }""",
        "TEST2": """{
            "en_passant": "STANDARD",
            "starting_pieces": "XKX,QXX",
            "move_set": "STANDARD",
            "attack_set": "NONE",
            "height": 5,
            "width": 3
        }""",
        "TEST3": """{
            "en_passant": "STANDARD",
            "starting_pieces": "RXXB,XBXX",
            "move_set": "STANDARD",
            "attack_set": "NONE",
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
        return self.ui_translated(self.games[game_id])

    def ui_translated(self, game_data):
        ui_game_data = copy.deepcopy(game_data)

        # Remove all board data except pieces
        board_data = ui_game_data['board']
        pieces_data = board_data['pieces']
        ui_game_data['pieces'] = pieces_data.copy()
        del ui_game_data['board']

        # Remove paths from piece data
        pieces_data = ui_game_data['pieces']
        for id in pieces_data.keys():
            piece_move_data = pieces_data[id]['valid_moves']
            valid_move_list = [i for i, _ in piece_move_data]
            pieces_data[id]['valid_moves'] = valid_move_list

        # Remove the move set
        del ui_game_data['rules']['move_set']

        return ui_game_data

    def start_game(self, ruleset='STANDARD', named_ruleset=None):
        # Choose game ID
        id = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

        curr_game = Game.start_new_game(ruleset)
        pprint.pprint(curr_game)

        self.games[id] = curr_game
        return id

    def make_move(self, game_id, move_data):
        game = Game(self.games[game_id])
        updated_game = game.make_move(move_data)
        self.games[game_id] = updated_game
        return self.ui_translated(updated_game)
