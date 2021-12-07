# AdvancedChess

Known bugs:
* A piece that can en passant another piece cannot use a non-capturing move to move into a square that would be a valid capture via en passant.
* En passant captures are not visible on the FE until the turn is passed, as they are calculated on the backend. This should be a straightforward fix of sending the en passant squares and last moved piece to the FE, and tagging each piece with if they can do en passant. It's just a question of if I ever put the time in to actually do that or not.
* I am bad at CSS, and can't get sizing to look good for both normal and Very Large boards.
