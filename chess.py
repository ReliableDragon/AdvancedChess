from collections import defaultdict
from game import Game

class Chess():
    games = defaultdict(lambda: {}, {
        "24601": {
            'width': 8,
            'height': 8,
            'pieces': [
                {'type': 'white_pawn', 'row': 0, 'column': 0, "valid_moves": [[0, 0]]},
                {'type': 'black_pawn', 'row': 0, 'column': 1, "valid_moves": [[0, 0]]},
                {'type': 'white_queen', 'row': 1, 'column': 0, "valid_moves": [[0, 0]]},
                {'type': 'black_queen', 'row': 1, 'column': 1, "valid_moves": [[0, 0]]},
                {'type': 'white_king', 'row': 7, 'column': 7, "valid_moves": [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7]], "valid_attacks": [[0, 1]]},
                ],
            'rules': {
                'en_passant': 'STANDARD',
                'starting_pieces': 'STANDARD',
            }
        }
    })

    def __init__(self):
        pass

    def get_state(self, game_id):
        return self.games[game_id]

    def start_game(self, rules):
