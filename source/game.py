"""Game module

This module contains the class Game which allow you to play chess.
He use the module rules to work and to know if everything is valid or not.
"""

import rules as ru

"""Constants"""
(   # This is what the move method can return.
INVALID_MOVE,
VALID_MOVE,
CHECK,
CHECK_MATE
) = range(4)


class Game:
    """The class Game contains all the mecanism to play chess."""

    def __init__(self):
        """Create the board, the player and initialize the history."""

        self.history = []
        self.undo_history = []
        self.board = ru.new_board(self.history);
        self.white_player = ru.Player(ru.WHITE_COLOR)
        self.black_plauer = ru.Plauer(ru.BLACK_COLOR)

    def get_board(self):
        """Return the board."""
        return self.board

    def undo(self):
        """Undo the last Move and store it in undo_history."""

    def redo(self):
        """Redo the last undone Move."""

    def move(self, color, (src_x, src_y), (dest_x, dest_y)):
        """Move the 'color' piece from (src_x, src_y) to (dest_x, dest_y).

        If the move is invalid, it return INVALID_MOVE.
        if the move is valid, it can return:
        VALID_MOVE if the piece moved.
        CHECK if now the ennemy of 'color is in check.
        CHECK mate if the 'color' won the game.
        """

