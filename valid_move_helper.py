from move import Move
import pprint

# piece: piece.Piece
# board: board.Board
# move_rules: dict (allowed moves, see DEFAULT_MOVE_MAP for example)
# returns: list[Move] (list of valid moves)
# If any more params get added,switch to a cfg = {} param approach, or refactor to class.
def get_valid_moves_for_piece(piece, board, move_rules, en_passant_allowed=False):
    valid_moves = set()
    piece_moves = move_rules[piece.type]
    # TODO: Add type == 'ACCELERATING', where the max_dist is equal to the number of times moved.
    for type, move in piece_moves.items():
        if type == 'DEFAULT':
            valid_moves |= iterate_move(piece, board, move, ep_ok=en_passant_allowed)
        if type == 'FIRST_MOVE' and piece.moves == 0:
            valid_moves |= iterate_move(piece, board, move, ep_ok=en_passant_allowed)
        if type == 'CAPTURE':
            valid_moves |= iterate_move(piece, board, move, capture=True, ep_ok=en_passant_allowed)
    return list(sorted(valid_moves))

# piece: dict/JSON
# board: board.Board
# move: dict (information about one specific type of move for a piece)
# capture: bool (if true, move must be a capture to be valid)
# return: set[Move] (valid moves w/rt board coords)
def iterate_move(piece, board, move, capture=False, ep_ok=False):
    valid_moves = set()
    for pattern in move['patterns']:
        valid_moves |= iterate_pattern(piece, board, pattern, move, capture_only=capture, ep_ok=ep_ok)
        if 'rotatable' in move:
            for rotated_pattern in generate_rotations(pattern):
                valid_moves |= iterate_pattern(piece, board, rotated_pattern, move, capture_only=capture, ep_ok=ep_ok)
    return valid_moves

# pattern: [(int, int)] (series of relative coords in a move option)
# return: arr[arr[int]] (pattern mirrored into quadrants 2, 3, and 4.)
def generate_rotations(pattern):
    return [[[p[1] * -1, p[0]] for p in pattern],
            [[p[0] * -1, p[1] * -1] for p in pattern],
            [[p[1], p[0] * -1] for p in pattern]]

# piece: dict/JSON
# board: board.Board
# pattern: arr[(int, int)] (deltas specifying one possible path for this move)
# move: dict (information about one specific type of move for a piece)
# capture: bool (if true, move must be a capture to be valid)
# returns: set[Move] (valid moves w/rt board coords)
def iterate_pattern(piece, board, pattern, move, capture_only=False, ep_ok=False):
    valid_moves = set()
    base = [piece.row, piece.col]
    color = piece.color
    jump = 'jump' in move

    min_dist, max_dist = None, None
    modulus = 1
    if move['distance'] == 'ANY':
        min_dist = 1
        max_dist = max(board.height, board.width)
    elif move['distance'][0] == 'MULTIPLESOF':
        modulus = move['distance'][1]
        min_dist = 1
        max_dist = max(board.height, board.width) * len(pattern)
    else:
        min_dist = move['distance'][0]
        max_dist = move['distance'][1]
        if max_dist == 'ANY':
            max_dist = max(board.height, board.width) * len(pattern)

    if min_dist > max_dist:
        return valid_moves

    i = 0
    path = []
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

            path += [tuple(curr_pos)]

            # Check distance
            if i < min_dist:
                continue
            if i % modulus != 0:
                continue
            if i > max_dist:
                stopped = True
                break

            # Check for move interruptions
            if board.off_board(curr_pos):
                stopped = True
                break
            elif is_ally(board, curr_pos, color):
                if jump:
                    continue
                else:
                    stopped = True
                    break
            elif is_enemy(board, curr_pos, color, ep_ok=ep_ok):
                if not 'noncapturing' in move:
                    valid_moves.add(Move(curr_pos, path[:-1].copy()))
                if not jump:
                    stopped = True
                    break
            elif not capture_only:
                valid_moves.add(Move(curr_pos, path[:-1].copy()))
        # If there's still move left, continue on from end of pattern.
        base = curr_pos.copy()

    return valid_moves

# curr_pos: (int, int) (board coord)
# board: board.Board
# returns: bool
def is_ally(board, curr_pos, curr_color):
    return board.get_at(curr_pos) != None and board.get_at(curr_pos).color == curr_color

# curr_pos: (int, int) (board coord)
# board: board.Board
# returns: bool
def is_enemy(board, curr_pos, curr_color, ep_ok=False):
    return ((board.get_at(curr_pos) != None and board.get_at(curr_pos).color != curr_color)
            or (ep_ok and board.en_passant_at(curr_pos)))
