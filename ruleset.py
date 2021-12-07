import logging
import move_maps

logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)

DEFAULT_RULES = {
    "en_passant": "STANDARD",
    "castling": "STANDARD",
    "starting_pieces": "STANDARD",
    "move_set": "STANDARD",
    "attack_set": "NONE",
    "victory_condition": "STANDARD",
    "movement_modifiers": "STANDARD",
    "height": 8,
    "width": 8,
    "moves_per_turn": 1,
}

NONE_EN_PASSANT_RULES = {
    "ATTACKERS": [],
    "VULNERABLE": [],
}

STANDARD_EN_PASSANT_RULES = {
    "ATTACKERS": ['P'],
    "VULNERABLE": ['P'],
}

ALWAYS_PAWNS_EN_PASSANT_RULES = {
    "ATTACKERS": ["P"],
    "VULNERABLE": ["P", "N", "B", "R", "Q", "K"],
}

ALWAYS_ALL_EN_PASSANT_RULES = {
    "ATTACKERS": ["P", "N", "B", "R", "Q", "K"],
    "VULNERABLE": ["P", "N", "B", "R", "Q", "K"],
}

class Ruleset():

    def __init__(self, rule_data):
        if rule_data == "STANDARD":
            rules = DEFAULT_RULES
        else:
            rules = rule_data.copy()
            for k, v in DEFAULT_RULES.items():
                if k not in rules.keys():
                    rules[k] = v

        self.en_passant = self.populate_en_passant(rules['en_passant'])
        self.starting_pieces = self.populate_piece_order(rules['starting_pieces'])
        self.height = rules['height']
        self.width = rules['width']
        self.castling = rules['castling']
        self.move_set = self.populate_move_set(rules['move_set'])
        self.attack_set = rules['attack_set']
        self.moves_per_turn = rules['moves_per_turn']

    def populate_move_set(self, move_set):
        print(f"Populating move set {move_set}")
        if isinstance(move_set, dict):
            # We've already processed this.
            return move_set
        elif move_set == 'STANDARD':
            return move_maps.STANDARD_MOVE_MAP
        elif move_set == 'TURBO':
            return move_maps.TURBO_MOVE_MAP
        elif move_set == 'SLOW':
            return move_maps.SLOW_MOVE_MAP
        elif move_set == 'CAPTURES_ONLY':
            return move_maps.CAPTURES_ONLY_MOVE_MAP
        elif move_set == 'JUMPY':
            return move_maps.JUMPY_MOVE_MAP
        elif move_set == 'CHAOS':
            return move_maps.gen_chaos_map()
        else:
            logger.warning(f"Received unknown move set {move_set}. Defaulting to STANDARD.")
            return move_maps.STANDARD_MOVE_MAP

    # ordering: str (represents a piece setup with the usual chess letter
    # abbreviations, and an X to represent no piece.)
    def populate_piece_order(self, ordering):
        result = None
        if isinstance(ordering, list):
            # We've already processed this.
            return ordering
        elif ordering == "STANDARD":
            result = ['RNBQKBNR', 'PPPPPPPP']
        else:
            result = ordering.split(',')

        return result

    def populate_en_passant(self, en_passant_rules):
        if isinstance(en_passant_rules, dict):
            return en_passant_rules
        elif en_passant_rules == "NONE":
            return NONE_EN_PASSANT_RULES
        elif en_passant_rules == "STANDARD":
            return STANDARD_EN_PASSANT_RULES
        elif en_passant_rules == "PAWNS":
            return ALWAYS_PAWNS_EN_PASSANT_RULES
        elif en_passant_rules == "ALL":\
            return ALWAYS_ALL_EN_PASSANT_RULES
        else:
            logger.warning(f"Received unsupported en passant setting: {en_passant_rules}. Using default rules.")
            return STANDARD_EN_PASSANT_RULES

    def can_be_en_passanted(self, piece_type):
        return piece_type in self.en_passant['VULNERABLE']

    def can_do_en_passant(self, piece_type):
        return piece_type in self.en_passant['ATTACKERS']

    def to_json_compatible(self):
        return {
                'en_passant': self.en_passant,
                'starting_pieces': self.starting_pieces,
                'height': self.height,
                'width': self.width,
                'castling': self.castling,
                'move_set': self.move_set,
                'attack_set': self.attack_set,
            }
