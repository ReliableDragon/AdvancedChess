import logging
import math
import sys

import tkinter as tk

from PIL import Image, ImageTk

# handler = logging.StreamHandler(sys.stdout)
# handler.setLevel(logging.DEBUG)

logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)
# logger.addHandler(handler)


PIECE_IMGS = {
    'WP': 'imgs/white_pawn.png',
    'WQ': 'imgs/white_queen.png',
    'WK': 'imgs/white_king.png',
    'WB': 'imgs/white_bishop.png',
    'WN': 'imgs/white_knight.png',
    'WR': 'imgs/white_rook.png',
    'BP': 'imgs/black_pawn.png',
    'BQ': 'imgs/black_queen.png',
    'BK': 'imgs/black_king.png',
    'BB': 'imgs/black_bishop.png',
    'BN': 'imgs/black_knight.png',
    'BR': 'imgs/black_rook.png',
}

class Render(tk.Canvas):

    SCALE = 100

    pattern_graphics = []
    images = []
    pieces = {}
    positions = {}

    def __init__(self, valid_moves, move_handler, params):
        self.valid_moves = valid_moves
        self.move_handler = move_handler
        self.params = params
        root = tk.Tk()
        root.title("Advanced Chess")
        root.resizable(0,0)
        self.screen_height = params.height * self.SCALE
        self.screen_width = params.width * self.SCALE
        tk.Canvas.__init__(self, root, bg='#FFFFFF', bd=0, height=self.screen_height, width=self.screen_width, highlightthickness=0)
        self.pack()
        self.bind("<Key>", self.enter)
        self.focus_set()
        self.display_message()
        self.draw_board()
        self.initialize_pieces()

        root.mainloop()

    def draw_board(self):
        logger.info("Drawing board.")
        for i in range(1, self.params.width):
            x_loc = i * self.screen_width / self.params.width
            self.create_line(
                x_loc,
                0,
                x_loc,
                self.screen_width)
        for i in range(1, self.params.height):
            y_loc = i * self.screen_height / self.params.height
            self.create_line(
                0,
                y_loc,
                self.screen_height,
                y_loc)

    def initialize_pieces(self):
        logger.info("Placing pieces")
        piece_order = self.params.get_piece_order()
        piece_size = math.floor(self.SCALE * 0.9)
        offset = math.floor(self.SCALE * 0.5)
        # White
        for j, row in enumerate(piece_order):
            for i, piece in enumerate(row):
                piece_name = 'W' + piece
                # logger.info(f"Placing {PIECE_IMGS[piece_name]}.")
                img = ImageTk.PhotoImage(Image.open(PIECE_IMGS[piece_name]).resize((piece_size, piece_size)))
                self.images.append(img)
                self.pieces[piece_name] = self.create_image(i * self.SCALE + offset, j * self.SCALE + offset, image=img)
                self.positions[(i, j)] = piece_name
        # Black
        for j, row in enumerate(piece_order):
            for i, piece in enumerate(row[::-1]):
                i_inv = self.params.height - i - 1
                j_inv = self.params.width - j - 1
                piece_name = 'B' + piece
                # logger.info(f"Placing {PIECE_IMGS[piece_name]}.")
                img = ImageTk.PhotoImage(Image.open(PIECE_IMGS[piece_name]).resize((piece_size, piece_size)))
                self.images.append(img)
                self.pieces[piece_name] = self.create_image(i_inv * self.SCALE + offset, j_inv * self.SCALE + offset, image=img)
                self.positions[(i_inv, j_inv)] = piece_name


    def handle_click(self, event):
        x = event.x
        y = event.y
        logger.info("Click at ({}, {})".format(x, y))
        cell = (math.floor(x / self.SCALE),
                math.floor(y / self.SCALE))
        if cell not in self.positions:
            logger.info("At {} there is nothing!".format(cell))
            return
        at_loc = self.positions[cell]
        logger.info("At {} is: {}".format(cell, at_loc))

    def enter(self, event):
        for i in self.pattern_graphics:
            self.delete(i)
        self.unbind("<Key>")
        self.bind("<Button-1>", self.handle_click)

    def display_message(self):
        self.pattern_graphics.append(
            self.create_text(
                self.screen_height * 0.5,
                self.screen_width * 0.5,
                text="Press any key to begin."))
