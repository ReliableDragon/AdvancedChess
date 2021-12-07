
def populate_valid_attacks(pieces, board, rules):
    for id, p in pieces.items():
        p['valid_attacks'] = get_valid_attacks(p, board, rules)

def get_valid_attacks(piece, board, rules):
    move_rules = rules['valid_attacks']
    if move_rules == 'STANDARD':
        pass
