import piece

class Board():

    # width: int
    # height: int
    # pieces: arr[dict/JSON]
    def __init__(self, width, height, pieces):
        assert(pieces is not None)
        self._board = {(p['row'], p['col']): piece.Piece(p['type'], p['color'], p['row'], p['col']) for p in pieces}
        self.width = width
        self.height = height

    # pos: (int, int) (board coord)
    # returns: Piece | None
    def get(self, pos):
        pos = tuple(pos)
        if pos not in self._board:
            return None
        else:
            return self._board[pos]

    # coord: (int, int)
    # returns: bool
    def off_board(self, coord):
        if coord[0] < 0 or coord[1] < 0 or coord[0] >= self.height or coord[1] >= self.width:
            return True
        else:
            return False
