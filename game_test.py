import unittest
import unittest.mock as mock
import logging
import sys

from unittest.mock import MagicMock
from game import Game
from move import Move

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

PAWNS_AND_KNIGHTS_RULES = """{
    "en_passant": "STANDARD",
    "starting_pieces": "XNX,XPX",
    "move_set": "STANDARD",
    "attack_set": "NONE",
    "height": 5,
    "width": 3
}"""

KINGS_AND_QUEENS_RULES = """{
    "en_passant": "STANDARD",
    "starting_pieces": "XKX,QXX",
    "move_set": "STANDARD",
    "attack_set": "NONE",
    "height": 5,
    "width": 3
}"""

BISHOPS_AND_ROOKS_RULES = """{
    "en_passant": "STANDARD",
    "starting_pieces": "RXXB,XBXX",
    "move_set": "STANDARD",
    "attack_set": "NONE",
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
        game_data = Game.start_new_game(PAWNS_AND_KNIGHTS_RULES)
        valid_moves = {id: n['valid_moves'] for id, n in game_data['pieces'].items()}
        self.assertDictEqual(
            valid_moves,
            {'black_N_0_1': [Move((2, 0), [(1, 1), (2, 1)]), Move((2, 2), [(1, 1), (2, 1)])], 'black_P_1_1': [Move((2, 1), [])], 'white_N_4_1': [Move((2, 0), [(3, 1), (2, 1)]), Move((2, 2), [(3, 1), (2, 1)])], 'white_P_3_1': [Move((2, 1), [])]})

    def test_queens_and_kings(self):
        game_data = Game.start_new_game(KINGS_AND_QUEENS_RULES)
        valid_moves = {id: n['valid_moves'] for id, n in game_data['pieces'].items()}
        self.assertEqual(
            valid_moves,
            {'black_K_0_1': [Move((0, 0), []), Move((1, 1), []), Move((0, 2), []), Move((1, 2), [])], 'black_Q_1_0': [Move((0, 0), []), Move((1, 1), []), Move((1, 2), [(1, 1)]), Move((2, 0), []), Move((3, 0), [(2, 0)]), Move((2, 1), []), Move((3, 2), [(2, 1)])], 'white_K_4_1': [Move((4, 0), []), Move((3, 1), []), Move((3, 2), []), Move((4, 2), [])], 'white_Q_3_0': [Move((4, 0), []), Move((1, 0), [(2, 0)]), Move((1, 2), [(2, 1)]), Move((2, 0), []), Move((2, 1), []), Move((3, 1), []), Move((3, 2), [(3, 1)])]})

    def test_bishops_and_rooks(self):
        game_data = Game.start_new_game(BISHOPS_AND_ROOKS_RULES)
        valid_moves = {id: n['valid_moves'] for id, n in game_data['pieces'].items()}
        self.assertDictEqual(
            valid_moves,
            {'black_R_0_0': [Move((0, 1), []), Move((1, 0), []), Move((2, 0), [(1, 0)]), Move((3, 0), [(1, 0), (2, 0)]), Move((0, 2), [(0, 1)]), Move((4, 0), [(1, 0), (2, 0), (3, 0)])], 'black_B_0_3': [Move((2, 1), [(1, 2)]), Move((3, 0), [(1, 2), (2, 1)]), Move((1, 2), [])], 'black_B_1_1': [Move((2, 0), []), Move((0, 2), []), Move((2, 2), []), Move((3, 3), [(2, 2)])], 'white_R_4_0': [Move((2, 0), [(3, 0)]), Move((0, 0), [(3, 0), (2, 0), (1, 0)]), Move((1, 0), [(3, 0), (2, 0)]), Move((3, 0), []), Move((4, 1), []), Move((4, 2), [(4, 1)])], 'white_B_4_3': [Move((2, 1), [(3, 2)]), Move((1, 0), [(3, 2), (2, 1)]), Move((3, 2), [])], 'white_B_3_1': [Move((2, 2), []), Move((4, 2), []), Move((1, 3), [(2, 2)]), Move((2, 0), [])]})

    def test_pawns_capture_and_double_move(self):
        game_data = Game.start_new_game(PAWN_CAPTURE_AND_CASTLE)
        print(game_data)
        valid_moves = {id: n['valid_moves'] for id, n in game_data['pieces'].items()}
        print(valid_moves)
        self.assertEqual(
            valid_moves,
            {'black_P_1_0': [Move((3, 0), [(2, 0)]), Move((2, 1), [])], 'black_P_1_1': [Move((2, 0), []), Move((3, 1), [(2, 1)])], 'white_P_2_0': [Move((1, 1), []), Move((0, 0), [(1, 0)])], 'white_P_2_1': [Move((0, 1), [(1, 1)]), Move((1, 0), [])]})
