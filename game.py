from board import Board
from ruleset import Ruleset
import coord
import piece_generator
import valid_move_helper
import string
import pprint

from invalid_move_error import InvalidMoveError

SWAP_TURN = {
    'white': 'black',
    'black': 'white',
}

class Game():
    def __init__(self, game_data):
        self.width = game_data['width']
        self.height = game_data['height']
        self.turn = game_data['turn']
        self.winner = game_data['winner']
        self.rules = Ruleset(game_data['rules'])
        self.board = Board(self.height, self.width, game_data['board'])
        self.move_counter = 0

    def swap_turn(self):
        if self.move_counter % self.rules.moves_per_turn == 0:
            self.turn = SWAP_TURN[self.turn]


    # game_data: dict/JSON{int: dict/JSON} (id to piece dict)
    # move_data: dict/JSON
    # returns: dict/JSON (updated game_data)
    def make_move(self, move_data):
        self.move_counter += 1
        # Extract salient data
        moving_piece_id = move_data['piece_id']
        row = move_data['row']
        col = move_data['col']
        # piece_data = game_data['pieces']
        moving_piece = self.board.get_id(moving_piece_id)
        valid_moves = moving_piece.valid_moves

        if moving_piece.color != self.turn:
            raise InvalidMoveError("Wrong color! It's not your turn!")

        valid_moves_list = [v for v in valid_moves if v.row == row and v.col == col]
        if not valid_moves_list:
            print(f"Attempted to move to {[row, col]}, when valid spaces were {valid_moves}")
            raise InvalidMoveError("Invalid move!")
        taken_move = valid_moves_list[0]

        # Will be empty if no captures
        captured_piece_id = self.board.capture_at((row, col))
        if captured_piece_id is not None:
            moving_piece.captures += 1
            self.board.remove_piece(captured_piece_id)

        # Update piece's position
        self.board.move_piece(moving_piece_id, row, col)
        moving_piece.moves += 1

        # Reset path for en passant
        self.board.remove_en_passant_path()
        if self.rules.can_be_en_passanted(moving_piece.type):
            self.board.add_en_passant_path(taken_move.path)

        for piece in self.board.pieces:
            en_passant_allowed = self.rules.can_do_en_passant(piece.type)
            piece.valid_moves = valid_move_helper.get_valid_moves_for_piece(piece, self.board, self.rules.move_set, en_passant_allowed)

        # Update board and regenerate valid moves, then return it
        # pieces = update_board(piece_data, game_data['rules'])
        self.swap_turn()
        return self.get_game_data()

    def get_game_data(self):
        return {
            'width': self.width,
            'height': self.height,
            'board': self.board.to_json_compatible(),
            'rules': self.rules.to_json_compatible(),
            'turn': self.turn,
            'winner': self.winner,
        }

    # rules: dict/JSON (see example above)
    # returns: (int, dict/JSON) (game ID, and dict containing all data about the game, to save in Firebase)
    # When starting a new game, there's no game_data to load from, so we use a static method.
    @staticmethod
    def start_new_game(rule_data):
        print("Starting new game with ruleset:")
        pprint.pprint(rule_data)
        rules = Ruleset(rule_data)

        # generated_piece_data = piece_generator.generate_starting_pieces(rules.height, rules.width, rules.starting_pieces)

        board = Board.from_starting_pieces(rules.height, rules.width, rules.starting_pieces)
        # board = Board(rules.height, rules.width, generated_piece_data)
        for piece in board.pieces:
            en_passant_allowed = rules.can_do_en_passant(piece.type)
            piece.valid_moves = valid_move_helper.get_valid_moves_for_piece(piece, board, rules.move_set, en_passant_allowed)

        game_data = {
            "width": rules.width,
            "height": rules.height,
            "board": board.to_json_compatible(),
            "rules": rules.to_json_compatible(),
            "turn": "white",
            "winner": "",
        }
        return game_data
