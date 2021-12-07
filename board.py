from piece import Piece
import pprint
import piece_generator

# self.height: int
# self.width: int
# self._board: dict{(int, int): Piece} (Piece objects by coordinate)
# self._pieces: dict{str: dict/JSON} (Piece data by ID)
class Board():

    # width: int
    # height: int
    # pieces: arr[dict/JSON]
    def __init__(self, height, width, board_data):
        self.height = height
        self.width = width
        self.en_passant_squares = board_data['en_passant_squares']
        self.last_moved_piece_id = board_data['last_moved_piece_id']
        self.populate_pieces(board_data['pieces'])

    def populate_pieces(self, pieces):
        assert(pieces is not None)
        self._board_by_loc = {}
        self._board_by_id = {}
        self.pieces = []
        # SHOULD BE DICT
        for id, piece_data in pieces.items():
            piece = Piece(piece_data)
            self._board_by_loc[(piece_data['row'], piece_data['col'])] = piece
            self._board_by_id[id] = piece
            self.pieces.append(piece)
        self._pieces = pieces.copy()

    # pos: [int, int] (board coord)
    # returns: Piece | None
    def get_at(self, pos):
        pos = tuple(pos)
        if pos not in self._board_by_loc:
            return None
        else:
            return self._board_by_loc[pos]

    # id: str (piece id)
    def get_id(self, id):
        if id not in self._board_by_id:
            return None
        else:
            return self._board_by_id[id]

    # coord: (int, int)
    # returns: bool
    def off_board(self, coord):
        if coord[0] < 0 or coord[1] < 0 or coord[0] >= self.height or coord[1] >= self.width:
            return True
        else:
            return False

    def add_en_passant_path(self, path):
        for p in path:
            self.en_passant_squares.append(p)

    def remove_en_passant_path(self):
        self.en_passant_squares = []

    def en_passant_at(self, coord):
        if tuple(coord) in self.en_passant_squares:
            return True
        else:
            return False

    def capture_at(self, coord):
        if coord in self.en_passant_squares:
            return self.last_moved_piece_id
        elif coord in self._board_by_loc:
            return self._board_by_loc[coord].id
        else:
            return None

    def move_piece(self, id, row, col):
        piece = self.get_id(id)
        del self._board_by_loc[piece.row, piece.col]
        piece.row = row
        piece.col = col
        self._board_by_loc[row, col] = piece
        self.last_moved_piece_id = id

    def remove_piece(self, id):
        piece = self.get_id(id)
        row = piece.row
        col = piece.col
        del self._board_by_loc[(row, col)]
        del self._board_by_id[id]
        self.pieces.remove(piece)

    def to_json_compatible(self):
        return {
            'en_passant_squares': self.en_passant_squares,
            'last_moved_piece_id': self.last_moved_piece_id,
            'pieces': {p.id: p.to_json_compatible() for p in self.pieces},
        }

    @staticmethod
    def from_starting_pieces(height, width, piece_ordering):
        generated_piece_data = piece_generator.generate_starting_pieces(piece_ordering, height, width)
        board_data = {
            'en_passant_squares': [],
            'last_moved_piece_id': None,
            'pieces': generated_piece_data,
        }
        return Board(height, width, board_data)
