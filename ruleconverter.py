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
        'id': f'{color}_{p}_{i_pos}_{j_pos}',
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
# returns: dict{int: dict/JSON} (dict of ids to chess pieces)
def generate_starting_pieces(piece_ordering, rules):
    pieces = {}
    height = rules['height']
    width = rules['width']
    for color in ['black', 'white']:
        for i, row in enumerate(piece_ordering):
            for j, p in enumerate(row):
                i_pos = i if color == 'black' else height - i - 1
                j_pos = j
                # Don't place pieces off the board.
                if i_pos > height - 1 or j_pos > width - 1:
                    continue
                # Don't place pieces on top of other pieces.
                if [p for p in pieces.values() if p['row'] == i_pos and p['col'] == j_pos]:
                    continue
                # Skip blanks.
                if p == 'X':
                    continue
                else:
                    piece = LETTER_TO_NAME_MAP[p]
                    initial_piece = generate_initial_piece(p, piece, color, i_pos, j_pos)
                    pieces[initial_piece['id']] = initial_piece
    return pieces

# pieces: dict{int: dict/JSON} (dict of ids to chess pieces)
# rules: dict/JSON (see default rules in game.py)
# returns: board.Board
def generate_board(pieces, rules):
    return board.Board(rules['width'], rules['height'], list(pieces.values()))

def populate_valid_attacks(pieces, board, rules):
    for id, p in pieces.items():
        p['valid_attacks'] = get_valid_attacks(p, board, rules)

def get_valid_attacks(piece, board, rules):
    move_rules = rules['valid_attacks']
    if move_rules == 'STANDARD':
        pass
