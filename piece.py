from move import Move
import pprint

class Piece():

    def __init__(self, piece_data):
        self.id = piece_data['id']
        self.icon = piece_data['icon']
        self.type = piece_data['type']
        self.color = piece_data['color']
        self.row = piece_data['row']
        self.col = piece_data['col']
        self.populate_valid_moves(piece_data['valid_moves'])
        self.valid_attacks = piece_data['valid_attacks']
        self.special = piece_data['special']
        self.moves = piece_data['moves']
        self.captures = piece_data['captures']
        self._piece_data = piece_data

    # moves: arr[(int, int), arr[int]] (list of coords for moves in slot 0, and paths in slot 1
    def populate_valid_moves(self, moves):
        # Initial game creation will not have valid moves.
        self.valid_moves = []
        if not moves:
            return
        for m in moves:
            # This is an awful hack, but we have to keep JSON compatibility...
            self.valid_moves.append(Move((m[0][0], m[0][1]), m[1]))

    def to_json_compatible(self):
        return {
            'id': self.id,
            'icon': self.icon,
            'type': self.type,
            'color': self.color,
            'row': self.row,
            'col': self.col,
            'valid_moves': [m.to_json_compatible() for m in self.valid_moves],
            'valid_attacks': self.valid_attacks,
            'special': self.special,
            'moves': self.moves,
            'captures': self.captures,
        }

    def __repr__(self):
        return str(self.to_json_compatible())

    def __str__(self):
        return str(self.to_json_compatible())
