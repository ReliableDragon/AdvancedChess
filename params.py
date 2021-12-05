

class Params():

    def __init__(self, height=8, width=8, piece_order="DEFAULT",
                en_passant="STANDARD"):
        self.height = height
        self.width = width
        self.piece_order = piece_order
        if not self.get_piece_order() or len(self.get_piece_order()[0]) != width:
            raise ValueError("Invalid piece ordering recieved!")

    def get_piece_order(self):
        if self.piece_order == "DEFAULT":
            return ['RNBQKBNR', 'PPPPPPPP']
        else:
            return piece_order.split('\n')
