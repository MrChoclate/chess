"""Rules module

This module contains the class Game which gathers all the necessary methods to
play chess.
"""
import sys
from collections import namedtuple

"""Constants"""
BOARD_SIZE = 8

(   # Color
WHITE_COLOR,
BLACK_COLOR
) = range(2)

(   # Piece type
PAWN,
BISHOP,
KNIGHT,
ROOK,
QUEEN,
KING
) = range(6)

(   # Move type
NORMAL_MOVE,
CAPTURE,
CASTLING,
EN_PASSANT,
PROMOTION
) = range(5)

Piece = namedtuple('Piece', 'type_, color')
Move  = namedtuple('Move', 'src, dest, type_')

"""Functions"""
def new_board():
    """Initialize the chessboard which is a dict"""
    b = {}

    for x in xrange(1, BOARD_SIZE+1):
        b[x, 2] = Piece(PAWN, WHITE_COLOR)
        b[x, 7] = Piece(PAWN, BLACK_COLOR)

    for x, type_ in enumerate([ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP,
                               KNIGHT, ROOK], start=1):
        b[x, 1] = Piece(type_, WHITE_COLOR)
        b[x, 8] = Piece(type_, BLACK_COLOR)

    return b

"""Class"""
class Game:
    """The class Game contains all the mecanism to play chess.

    board is a dict which contains the chessboard.
    history is a list of Move.
    undo_history is a list of undone Move.
    white_captured_pieces is a list of all white pieces which are taken.
    black_captured_pieces is a list of all black pieces which are taken.
    """

    def __init__(self):
        """Create the board and initialize the history."""

        self.board = new_board();
        self.history = []
        self.undo_history = []
        self.white_captured_pieces = []
        self.black_captured_pieces = []

    def _can_piece_move(self, (s_x, s_y), (d_x, d_y)):
        """Say if the piece at (s_x, s_y) can go to (d_x, d_y).

        Return the Move if the piece can move, else return False.
        """

    def _capture(self, (x, y)):
        """Capture the piece at (x, y) and store it in the right list."""

        assert((x, y) in self.board)
        if(self.board[x, y].color == WHITE_COLOR):
            self.white_captured_pieces.append(self.board[x, y])
        elif(self.board[x, y].color == BLACK_COLOR):
            self.black_captured_pieces.append(self.board[x, y])
        else:
            sys.exit("Unknown piece color")

    def _capture_en_passant(self, color, (x, y)):
        """Capture the piece when the 'color' pawn goes to (x, y)."""

        if(color == WHITE_COLOR):
            y -= 1
        elif(color == BLACK_COLOR):
            y += 1
        else:
            sys.exit("Unknown player color")

        self._capture((x,y))

    def _where_is_king(self, color):
        """Return the position of the king color"""

        for pos, piece in self.board.iteritems():
            if(piece.type_ == KING & piece.color = color):
                return pos

        # Error message
        if(color == WHITE_COLOR):
            c = "white"
        elif(color == BLACK_COLOR):
            c = "black"
        else:
            sys.exit("Unknown player color")
        sys.exit("Error, "+c+" king not found")

    def is_check(self, color):
        """Return True if the 'color' king is in check"""

    def is_check_mate(self, color):
        """Return True if the 'color' king is check mate"""

        if not self.is_check(color):
            return False

    def undo(self):
        """Undo the last Move and store it in undo_history"""

    def redo(self):
        """Redo the last undone Move"""

    def move(self, color, (src_x, src_y), (dest_x, dest_y)):
        """Move the 'color' piece from (src_x, src_y) to (dest_x, dest_y).

        The piece must be of the color 'color'.
        Return True if the piece has been successfully moved.
        """

        # Test if the parameters are wrongs
        if color not in [WHITE_COLOR, BLACK_COLOR]:
            return False
        if (src_x or src_y or dest_x or dest_y) not in range(1, BOARD_SIZE+1):
            return False
        if(self.board[src_x, src_y].color != color):
            return False
        if((dest_x, dest_y) in self.board and
                                    self.board[dest_x, dest_y].color == color):
            return False

        # Store the Move in m
        m = self._can_piece_move((src_x, src_y), (dest_x, dest_y))
        if(type(m) == bool or type(m) != type(Move)):
            return False

        # Move the piece
        if(m.type_ == CAPTURE):
            self._capture(dest_x, dest_y)
        if(m.type_ == EN_PASSANT):
            self._capture_en_passant(color, (dest_x, dest_y))
        board[dest_x, dest_y] = board[src_x, src_y]
        del board[src_x, src_y]

        # If 'color' is in check, undo the move
        if(self.is_check(color)):
            self.undo()
            undo_history.pop
            return False

        del undo_history
        return True
