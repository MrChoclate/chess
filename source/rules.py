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
PROMOTION,
CAPTURE_PROMOTION
) = range(6)

Piece = namedtuple('Piece', 'type_, color')
Move  = namedtuple('Move', 'src, dest, type_')

"""Functions"""
def new_board():
    """Initialize the chessboard which is a dict"""
    b = {}

    for x in xrange(1, BOARD_SIZE+1):
        b[x, 2] = Piece(PAWN, WHITE_COLOR)
        b[x, BOARD_SIZE-1] = Piece(PAWN, BLACK_COLOR)

    for x, type_ in enumerate([ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP,
                               KNIGHT, ROOK], start=1):
        b[x, 1] = Piece(type_, WHITE_COLOR)
        b[x, BOARD_SIZE] = Piece(type_, BLACK_COLOR)

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

        Return the Move if the piece can, else return False.
        """

        color = self.board[s_x, s_y].color

        if(self.board[s_x, s_y].type_ == PAWN):
            return self._can_pawn_move(color, (s_x, s_y), (d_x, d_y))
        elif(self.board[s_x, s_y].type_ == BISHOP):
            return self._can_bishop_move(color, (s_x, s_y), (d_x, d_y))
        elif(self.board[s_x, s_y].type_ == KNIGHT):
            return self._can_knight_move(color, (s_x, s_y), (d_x, d_y))
        elif(self.board[s_x, s_y].type_ == ROOK):
            return self._can_rook_move(color, (s_x, s_y), (d_x, d_y))
        elif(self.board[s_x, s_y].type_ == QUEEN):
            return self._can_queen_move(color, (s_x, s_y), (d_x, d_y))
        elif(self.board[s_x, s_y].type_ == KING):
            return self._can_king_move(color, (s_x, s_y), (d_x, d_y))



    def _castling(color, (x, y)):
        """Move the rook on the other side of the king position (x, y)."""

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

    m = history.pop
    undo_history.append(m)
    color = self.board[m.dest].color

    # Undo a normal move
    self.board[m.src] = self.board[m.dest]
        del self.board[m.dest]
    # Undo a capture
    elif(m.type_ = CAPTURE):
        if(color = WHITE_COLOR):
            self.board[m.dest] = black_captured_pieces.pop()
        elif(color = BLACK_COLOR):
            self.board[m.dest] = white_captured_pieces.pop()
        else:
            sys.exit("Unknown piece color")
    # Undo a castling
    elif(m.type_ = CASTLING):
        (x, y) = m.dest
        if(x = 3):
            self.board[1, y] = self.board[x+1, y]
            del self.board[x+1, y]
        elif(x = 7):
            self.board[BOARD_SIZE, y] = self.board[x-1, y]
            del self.board[x-1, y]
        else:
            sys.exit("Can't undo castling move")
    # Undo a promotion without capture
    elif(m.type_ = PROMOTION):
        self.board[m.src].type_ = PAWN
    # Undo a promotion with capture
    elif(

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
        if(type(m) == bool):
            return False
        if(type(m) != type(Move)):
            sys.exit("Unknown type of move")

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

class Rules():
    """The class Rules contains all technical methods to play"""


class Piece(Rules):
    """The class Piece represents a piece in a chess game.

    All can capture an ennemy piece.
    """

    def __init__(self, type_, color, board, history):
        self.type_ = type_
        self.color = color
        self.board = board
        self.history = history

    def capture(self, (x, y)):
        """Capture the piece at (x, y) and store it in the right list."""

        assert((x, y) in self.board)
        if(self.board[x, y].color == WHITE_COLOR):
            self.white_captured_pieces.append(self.board[x, y])
        elif(self.board[x, y].color == BLACK_COLOR):
            self.black_captured_pieces.append(self.board[x, y])
        else:
            sys.exit("Unknown piece color")

class Pawn(Piece):
    """The class Pawn represents a pawn in chess game.

    Pawn have two special moves: promotion and 'en passant'.
    """

    def __init__(self, color, board, history):
        self.color = color
        self.board = board
        self.history = history

    def promote(self, (x, y), type_):
        """!!!Transform the pawn at (x, y) into type_ !!!
        This method shouldn't be there !!!
        """

    def capture_en_passant(self, (x, y)):
        """Capture the piece when the 'color' pawn goes to (x, y)."""

        if(self.color == WHITE_COLOR):
            y -= 1
        elif(self.color == BLACK_COLOR):
            y += 1
        else:
            sys.exit("Unknown player color")

        self.capture((x,y))

    def can_move(self, (s_x, s_y), (d_x, d_y)):
        """Say if the pawn at (s_x, s_y) can go to (d_x, d_y).

        Pawn have a special move called 'en passant'.
        Return the Move if the pawn can, else return False.
        """

class Bishop(Piece):
    """The class Bishop represents a bishop in chess Game.

    The Bishop have only normal move.
    """

    def __init__(self, color, board):
        self.color = color
        self.board = board

    def can_move(self, (s_x, s_y), (d_x, d_y)):
        """Say if the bishop at (s_x, s_y) can go to (d_x, d_y).

        Return the Move if the bishop can, else return False.
        """

class Knight(Piece):
    """The class Knight represents a knight in chess game.

    The knight have only normal move.
    """

    def __init__(self, color, board):
        self.color = color
        self.board = board

    def can_move(self, (s_x, s_y), (d_x, d_y)):
        """Say if the knight at (s_x, s_y) can go to (d_x, d_y).

        Return the Move if the knight can, else return False.
        """

class Rook(Piece):
    """The class Rook represents a rook in chess game.

    Rook have a special move shared with the king called castling.
    """

    def __init__(self, color, board, history):
        self.color = color
        self.board = board
        self.history = history

    def castling(self, (x, y)):
        """Move the rook at (x, y) and move the king to perform a castling.

        It assumes that the rook can castling.
        """

    def can_move(self, (s_x, s_y), (d_x, d_y), history):
        """Say if the rook at (s_x, s_y) can go to (d_x, d_y).

        Return the Move if the rook can, else return False.
        """

class Queen(Piece):
    """The class Queen represents a queen in chess game.

    The queen have no special move.
    """
    def __init__(self, color, board):
        self.color = color
        self.board = board

    def can_move(self, (s_x, s_y), (d_x, d_y)):
        """Say if the queen at (s_x, s_y) can go to (d_x, d_y).

        Return the Move if the queen can, else return False.
        """
class King(Piece):
    """The class King represents a king in chess game.

    The king can perform castling.
    """
    def __init__(self, color, board, history)
        self.color = color
        self.board = board
        self.history = history

    def castling(self, (x, y)):
        """Move the king to (x, y) and move the rook to perform a castling.

        It is assumed that king can castling.
        """

    def can_king_move(self, (s_x, s_y), (d_x, d_y), history):
        """Say if the king at (s_x, s_y) can go to (d_x, d_y).

        Return the Move if the king can, else return False.
        """
