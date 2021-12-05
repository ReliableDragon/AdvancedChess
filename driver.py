import logging
import sys

from params import Params
import render

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class RunChessCLI():
    def __init__(self):
        logger.info("Initializing chess.")
        self.params = Params()

        def valid_moves(piece, loc):
            self.valid_moves(piece, loc)

        def handle_moves(move):
            self.move(move)

        self.renderer = render.Render(valid_moves, handle_moves, self.params)

    def play(self):
        logger.info("Starting play!")

    def valid_moves(self, piece, loc):
        logger.info(f"Fetching valid moves for {pices} at {loc}")

    def move(self, move):
        logger.info(f"Recieved move: {move}")


if __name__ == "__main__":
    driver = RunChessCLI()
    driver.play()
