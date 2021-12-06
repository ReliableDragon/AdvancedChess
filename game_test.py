import unittest
import unittest.mock as mock
import logging
import sys

from unittest.mock import MagicMock
from game import Game

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

PAWNS_AND_KNIGHTS_RULES = """{
    "en_passant": "STANDARD",
    "starting_pieces": "XNX,XPX",
    "move_set": "STANDARD",
    "valid_attacks": "NONE",
    "attack_set": "STANDARD",
    "height": 5,
    "width": 3
}"""

KINGS_AND_QUEENS_RULES = """{
    "en_passant": "STANDARD",
    "starting_pieces": "XKX,QXX",
    "move_set": "STANDARD",
    "valid_attacks": "NONE",
    "attack_set": "STANDARD",
    "height": 5,
    "width": 3
}"""

BISHOPS_AND_ROOKS_RULES = """{
    "en_passant": "STANDARD",
    "starting_pieces": "RXXB,XBXX",
    "move_set": "STANDARD",
    "valid_attacks": "NONE",
    "attack_set": "STANDARD",
    "height": 5,
    "width": 4
}"""

PAWN_CAPTURE_AND_CASTLE = """{
    "starting_pieces": "XXX,PPX",
    "height": 4,
    "width": 3
}"""

class TestNewGame(unittest.TestCase):

    def test_pawns_noncapturing_and_basic_knights(self):
        id, game_data = Game.new_game(PAWNS_AND_KNIGHTS_RULES)
        valid_moves = {n['id']: n['valid_moves'] for n in game_data['pieces']}
        self.assertEqual(
            valid_moves,
            {'white_N01': [[2, 2], [2, 0]], 'white_P11': [[2, 1]], 'black_N41': [[2, 2], [2, 0]], 'black_P31': [[2, 1]]})

    def test_queens_and_kings(self):
        id, game_data = Game.new_game(KINGS_AND_QUEENS_RULES)
        valid_moves = {n['id']: n['valid_moves'] for n in game_data['pieces']}
        self.assertEqual(
            valid_moves,
            {'white_K01': [[1, 1], [0, 2], [0, 0], [1, 2]], 'white_Q10': [[2, 0], [3, 0], [4, 0], [1, 1], [1, 2], [0, 0], [2, 1], [3, 2]], 'black_K41': [[3, 1], [4, 2], [4, 0], [3, 0]], 'black_Q32': [[2, 2], [1, 2], [0, 2], [4, 2], [3, 1], [3, 0], [2, 1], [1, 0]]})

    def test_bishops_and_rooks(self):
        id, game_data = Game.new_game(BISHOPS_AND_ROOKS_RULES)
        valid_moves = {n['id']: n['valid_moves'] for n in game_data['pieces']}
        self.assertEqual(
            valid_moves,
            {'white_R00': [[1, 0], [2, 0], [3, 0], [4, 0], [0, 1], [0, 2]], 'white_B03': [[1, 2], [2, 1], [3, 0]], 'white_B11': [[2, 2], [3, 3], [0, 2], [2, 0]], 'black_R43': [[3, 3], [2, 3], [1, 3], [0, 3], [4, 2], [4, 1]], 'black_B40': [[3, 1], [2, 2], [1, 3]], 'black_B32': [[2, 3], [4, 1], [2, 1], [1, 0]]})

    def test_pawns_capture_and_double_move(self):
        id, game_data = Game.new_game(PAWN_CAPTURE_AND_CASTLE)
        valid_moves = {n['id']: n['valid_moves'] for n in game_data['pieces']}
        self.assertEqual(
            valid_moves,
            {'white_P10': [[2, 0], [3, 0], [2, 1]], 'white_P11': [[3, 1], [2, 2]], 'black_P22': [[1, 2], [0, 2], [1, 1]], 'black_P21': [[0, 1], [1, 0]]})
