import board

LETTER_TO_NAME_MAP = {
    'P': 'pawn',
    'N': 'knight',
    'B': 'bishop',
    'R': 'rook',
    'Q': 'queen',
    'K': 'king',
}

NAME_TO_LETTER_MAP = {
    'pawn': 'P',
    'knight': 'N',
    'bishop': 'B',
    'rook': 'R',
    'queen': 'Q',
    'king': 'K',
}


# ordering: str (represents a piece setup with the usual chess letter
# abbreviations, and an X to represent no piece.)
def get_piece_order(ordering):
    result = None
    if ordering == "STANDARD":
        result = ['RNBQKBNR', 'PPPPPPPP']
    else:
        result = ordering.split(',')

    return result

# p: str (chess letter abbreviation)
# piece: str (full name of piece)
# color: str
# i_pos: int
# j_pos: int
# returns: dict/JSON (represents a chess piece)
def generate_initial_piece(p, piece, color, i_pos, j_pos):
    return {
        'id': f'{color}_{p}_{i_pos}{j_pos}',
        'icon': f'{color}_{piece}',
        'type': p,
        'color': color,
        'row': i_pos,
        'col': j_pos,
        'valid_moves': None,
        'valid_attacks': None,
        'special': None,
        'moves': 0,
        'captures': 0,
    }

# piece_ordering: str (see get_piece_order)
# rules: dict/JSON (see default rules in game.py)
# returns: arr[dict/JSON] (array of chess pieces)
def generate_starting_pieces(piece_ordering, rules):
    pieces = []
    for color in ['black', 'white']:
        # if color == 'black':
        #     piece_ordering = map(reversed, piece_ordering)
        for i, row in enumerate(piece_ordering):
            for j, p in enumerate(row):
                i_pos = i if color == 'black' else rules['height'] - i - 1
                j_pos = j
                if p == 'X':
                    continue
                else:
                    piece = LETTER_TO_NAME_MAP[p]
                    pieces.append(generate_initial_piece(p, piece, color, i_pos, j_pos))
    return pieces

# pieces: arr[dict/JSON] (array of chess pieces)
# rules: dict/JSON (see default rules in game.py)
# returns: board.Board
def generate_board(pieces, rules):
    # board = [[None for _ in rules['width']] for _ in rules['height']]
    # for p in pieces:
    #     board[p.row][p.col] = Piece.Piece(p.type, p.color, p.row, p.col)
    return board.Board(rules['width'], rules['height'], pieces)

def populate_valid_attacks(pieces, board, rules):
    for p in pieces:
        p['valid_attacks'] = get_valid_attacks(p, board, rules)

def get_valid_attacks(piece, board, rules):
    move_rules = rules['valid_attacks']
    if move_rules == 'STANDARD':
        pass
