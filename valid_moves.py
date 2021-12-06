# Moves must be defined in the first quadrant (assuming you're sitting at the
# board facing your opponent) to be reflected properly.
DEFAULT_MOVE_MAP = {
    'P': {
        'DEFAULT': {
            'patterns': [[[1, 0]]],
            'distance': [1, 1],
            'noncapturing': True
        },
        'FIRST_MOVE': {
            'patterns': [[[1, 0]]],
            'distance': [2, 2],
            'noncapturing': True
        },
        'CAPTURE': {
            'patterns': [[[1, 1]], [[1, -1]]],
            'distance': [1, 1],
        },
    },
    'N': {
        'DEFAULT': {
            'patterns': [[[1, 0], [2, 0], [2, 1]], [[1, 0], [2, 0], [2, -1]]],
            'distance': [3, 3],
            'rotatable': True,
            'jump': True,
        }
    },
    'B': {
        'DEFAULT': {
            'patterns': [[[1, 1]]],
            'distance': 'ANY',
            'rotatable': True,
        }
    },
    'R': {
        'DEFAULT': {
            'patterns': [[[1, 0]]],
            'distance': 'ANY',
            'rotatable': True,
        }
    },
    'Q': {
        'DEFAULT': {
            'patterns': [[[1, 0]], [[1, 1]]],
            'distance': 'ANY',
            'rotatable': True,
        }
    },
    'K': {
        'DEFAULT': {
            'patterns': [[[1, 0]], [[1, 1]]],
            'distance': [1, 1],
            'rotatable': True,
        }
    },
}

# pieces: arr[dict/JSON]
# board: board.Board
# rules: dict/JSON
# returns: arr[dict/JSON]
def populate_valid_moves(pieces, board, rules):
    move_rules = rules['move_set']
    if move_rules == 'STANDARD':
        move_rules = DEFAULT_MOVE_MAP
    for i, piece in enumerate(pieces):
        pieces[i]['valid_moves'] = get_valid_moves(piece, board, move_rules)
    return pieces
# piece: dict/JSON
# board: board.Board
# move_rules: dict (allowed moves, see DEFAULT_MOVE_MAP for example)
# returns: arr[(int, int)] (array of valid moves coords on board)
def get_valid_moves(piece, board, move_rules):
    valid_moves = []
    piece_moves = move_rules[piece['type']]
    for type, move in piece_moves.items():
        if type == 'DEFAULT':
            valid_moves += iterate_move(piece, board, move)
        if type == 'FIRST_MOVE' and piece['moves'] == 0:
            valid_moves += iterate_move(piece, board, move)
        if type == 'CAPTURE':
            valid_moves += iterate_move(piece, board, move, capture=True)
    return valid_moves

# pattern: [(int, int)] (series of relative coords in a move option)
def generate_rotations(pattern):
    return [[[p[1] * -1, p[0]] for p in pattern],
            [[p[0] * -1, p[1] * -1] for p in pattern],
            [[p[1], p[0] * -1] for p in pattern]]

# piece: dict/JSON
# board: board.Board
# move: dict (information about one specific type of move for a piece)
# capture: bool (if true, move must be a capture to be valid)
def iterate_move(piece, board, move, capture=False):
    valid_moves = []
    for pattern in move['patterns']:
        valid_moves += iterate_pattern(piece, board, pattern, move, capture_only=capture)
        if 'rotatable' in move:
            for rotated_pattern in generate_rotations(pattern):
                valid_moves += iterate_pattern(piece, board, rotated_pattern, move, capture_only=capture)
    return valid_moves

# curr_pos: (int, int) (board coord)
# board: board.Board
# returns: bool
def is_ally(board, curr_pos, curr_color):
    return board.get(curr_pos) != None and board.get(curr_pos).color == curr_color

 # curr_pos: (int, int) (board coord)
 # board: board.Board
 # returns: bool
def is_enemy(board, curr_pos, curr_color):
    return board.get(curr_pos) != None and board.get(curr_pos).color != curr_color

# piece: dict/JSON
# board: board.Board
# pattern: arr[(int, int)] (deltas specifying one possible path for this move)
# move: dict (information about one specific type of move for a piece)
# capture: bool (if true, move must be a capture to be valid)
# returns: arr[(int, int)] (valid moves w/rt board coords)
def iterate_pattern(piece, board, pattern, move, capture_only=False):
    valid_moves = []
    base = [piece['row'], piece['col']]
    color = piece['color']
    jump = 'jump' in move

    min_dist, max_dist = None, None
    if move['distance'] == 'ANY':
        min_dist = 1
        max_dist = max(board.height, board.width)
    else:
        min_dist = move['distance'][0]
        max_dist = move['distance'][1]
        if max_dist == 'ANY':
            max_dist = max(board.height, board.width)

    i = 0
    stopped = False
    while not stopped:
        for step in pattern:
            i += 1
            curr_pos = base.copy()
            # Invert direction for white player
            dy = step[0] if color == 'black' else step[0] * -1
            dx = step[1]
            curr_pos[0] += dy
            curr_pos[1] += dx

            # Check distance
            if i < min_dist:
                continue
            if i > max_dist:
                stopped = True
                break

            # Check for move interruptions
            if board.off_board(curr_pos):
                stopped = True
                break
            if is_ally(board, curr_pos, color):
                if jump:
                    continue
                else:
                    stopped = True
                    break
            if is_enemy(board, curr_pos, color):
                if not 'noncapturing' in move:
                    valid_moves.append(curr_pos)
                if not jump:
                    stopped = True
                    break
            if not capture_only:
                valid_moves.append(curr_pos)
        # If there's still move left, continue on from end of pattern.
        base = curr_pos.copy()

    return valid_moves
