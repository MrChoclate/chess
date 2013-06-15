"""Rules module

This module contains the class Rules to know all the rules to play chess.
"""

import sys
from collections import namedtuple

"""Constants"""
BOARD_SIZE = 8
WHITE_PAWN_ROW = 2
BLACK_PAWN_ROW = 7
WHITE_PAWN_DIRECTION = 1
BLACK_PAWN_DIRECTION = -1

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

Move = namedtuple('Move', 'src, dest, type_')

"""Functions"""
def new_board(history):
    """Initialize the chessboard which is a dict.

    The parameter history is used to bound the history to the pieces.
    """
    b = {}

    for x in xrange(1, BOARD_SIZE+1):
        b[x, WHITE_PAWN_ROW] = Piece(PAWN, WHITE_COLOR, b, history).create()
        b[x, BLACK_PAWN_ROW] = Piece(PAWN, BLACK_COLOR, b, history).create()

    for x, type_ in enumerate([ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP,
                               KNIGHT, ROOK], start=1):
        b[x, 1] = Piece(type_, WHITE_COLOR, b, history).create()
        b[x, BOARD_SIZE] = Piece(type_, BLACK_COLOR, b, history).create()

    return b

def enemy_color(color):
    """Return the enemy color of 'color'."""

    if(color == WHITE_COLOR):
        return BLACK_COLOR
    if(color == BLACK_COLOR):
        return WHITE_COLOR
    sys.exit("Unknown color while looking for the enemy color")

"""Classes"""
class Board():
    """The class Board represents a board as a dict.
    
    It gathers all the methods wich only need the board.
    """
    
    def __init__(self, history):
        self.dict_ = new_board(history)

    """The class board acts like a dict"""
    def __getitem__(self, key):
        return self.dict_[key]
    def __setitem__(self, key, value):
        self.dict_[key] = value
    def __delitem__(self, key):
        del self.dict_[key]
    def __contains__(self, key):
        return key in self.dict_

    def where_is_king(self, color):
    """Return the coordinates of the 'color' king."""

        for (x, y), p in self.dict_.iteritems():
            if(p.get_type == KING and p.color == color):
                return (x, y)

        # Error message
        if(color == WHITE_COLOR):
            s = "White"
        elif(color == BLACK_COLOR):
            s = "Black"
        else:
            sys.exit("Unknown color while looking for the king's position")
        sys.exit(s + " king not found")

    def who_controls(self, (x, y), color):
        """Return the list of 'color' pieces which control the coordinates
        (x, y).
        """

    def is_check(self, color):
        """Return True if the 'color' king is in check."""

        if(self.is_controlled(self.where_is_king(color), enemy_color(color))):
            return True
        else:
            return False

    def is_check_mate(self, color):
        """Return True if the 'color' king is check mate.

        It is assumed that the king is already in check.
        """

    def promote(self, (x, y), type_):
        """Transform the pawn at (x, y) into type_.

        type_ must be different of PAWN.
        """

        assert((x, y) in self.dict_ and self.dict_[x, y].get_type() == PAWN and
               type_ != PAWN)

        c, h = self.dict_[x, y].color, self.dict_[x, y].history
        self.dict_[x, y] = Piece(type_, c, self.dict_, h).create()


class Piece():
    """The class Piece should only be used to create a piece.

    It give to all pieces the capture and get_type methods.
    """

    def __init__(self, type_, color, board, history):
        self.type_ = type_
        self.color = color
        self.board = board
        self.history = history

    def create(self):
        """Return the type_ piece"""

        if(self.type_ == PAWN):
            return Pawn(self.color, self.board, self.history)
        if(self.type_ == BISHOP):
            return Bishop(self.color, self.board)
        if(self.type_ == KNIGHT):
            return Knight(self.color, self.board)
        if(self.type_ == ROOK):
            return Rook(self.color, self.board, self.history)
        if(self.type_ == QUEEN):
            return Queen(self.color, self.board)
        if(self.type_ == KING):
            return King(self.color, self.board, self.history)

        sys.exit("Unknown piece type while creating it")

    def capture(self, player, (x, y)):
        """The player 'player' capture the piece at (x, y) and store it in his 
        list."""

        assert((x, y) in self.board and self.board[x, y].color != player.color)
        player.captured_pieces.append(self.board[x, y])
        del self.board[x, y]

    def get_type(self):
        """Return the type of the piece."""
        
        return self.type_

class Pawn(Piece):
    """The class Pawn represents a pawn in chess game.

    Pawn have two special moves: promotion and 'en passant'.
    """

    def __init__(self, color, board, history):
        self.color = color
        self.board = board
        self.history = history
        self.type_ = PAWN

    def get_direction(self):
        """Return the pawn direction depending on his color."""
        
        if(self.color == WHITE_COLOR):
            return WHITE_PAWN_DIRECTION
        if(self.color == BLACK_PAWN_DIRECTION):
            return BLACK_PAWN_DIRECTION
        sys.exit("Unknown color while looking for the direction of the pawn")

    def capture_en_passant(self, player, (x, y)):
        """Capture the piece when the pawn of player goes to (x, y)."""

        assert(player.color == self.color)

        if(player.color == WHITE_COLOR):
            y -= 1
        elif(player.color == BLACK_COLOR):
            y += 1
        else:
            sys.exit("Unknown player color")

        self.capture(player, (x,y))

    def can_move(self, (s_x, s_y), (d_x, d_y)):
        """Say if the pawn at (s_x, s_y) can go to (d_x, d_y).

        Pawn have two special moves called 'en passant' and promotion.
        Return the Move if the pawn can, else return False.
        """

        d = self.get_direction()


class Bishop(Piece):
    """The class Bishop represents a bishop in chess Game.

    The Bishop have only normal move.
    """

    def __init__(self, color, board):
        self.color = color
        self.board = board
        self.type_ = BISHOP

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
        self.type_ = KNIGHT

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
        self.type_ = ROOK

    def castling(self, (x, y)):
        """Move the rook at (x, y) and move the king to perform a castling.

        It assumes that the rook can castling.
        """

    def can_move(self, (s_x, s_y), (d_x, d_y)):
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
        self.type_ = QUEEN
        
    def can_move(self, (s_x, s_y), (d_x, d_y)):
        """Say if the queen at (s_x, s_y) can go to (d_x, d_y).

        Return the Move if the queen can, else return False.
        """
class King(Piece):
    """The class King represents a king in chess game.

    The king have a special move shared with the rook called castling.
    """
    def __init__(self, color, board, history):
        self.color = color
        self.board = board
        self.history = history
        self.type_ = KING

    def castling(self, (x, y)):
        """Move the king to (x, y) and move the rook to perform a castling.

        It is assumed that king can castling.
        """

    def can_move(self, (s_x, s_y), (d_x, d_y)):
        """Say if the king at (s_x, s_y) can go to (d_x, d_y).

        Return the Move if the king can, else return False.
        """
