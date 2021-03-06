"""Rules module

This module contains the class Rules to know all the rules to play chess.
"""

import sys
from collections import namedtuple
from math import copysign

"""Constants"""
BOARD_SIZE = 8
WHITE_KING_POS = (5, 1)
BLACK_KING_POS = (5, 8)

KINGSIDE_KING_POS_X = 7
QUEENSIDE_KING_POS_X = 3
KINGSIDE_ROOK_POS_X = 6
QUEENSIDE_ROOK_POS_X = 4

WHITE_PAWN_ROW = 2
BLACK_PAWN_ROW = 7
WHITE_PAWN_DIRECTION = 1
BLACK_PAWN_DIRECTION = -1

CARDINAL_DIRECTION = [(1, 0), (-1, 0), (0, 1), (0, -1)]
FOUR_DIAGONALS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
KNIGHT_MOVES = [(1,2), (2,1), (-1,2), (-2,1), (1,-2), (2,-1), (-1,-2),
                                                                     (-2,-1)]

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
def new_board(B, history):
    """Initialize the chessboard which is a dict.

    The parameter history and B is used to bound the history and the class
    Board to the pieces.
    """
    
    b = {}

    for x in xrange(1, BOARD_SIZE+1):
        b[x, WHITE_PAWN_ROW] = Piece(PAWN, WHITE_COLOR, B, history).create()
        b[x, BLACK_PAWN_ROW] = Piece(PAWN, BLACK_COLOR, B, history).create()

    for x, type_ in enumerate([ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP,
                               KNIGHT, ROOK], start=1):
        b[x, 1] = Piece(type_, WHITE_COLOR, B, history).create()
        b[x, BOARD_SIZE] = Piece(type_, BLACK_COLOR, B, history).create()

    return b
    
def get_path((s_x, s_y), (d_x, d_y)):
    """Return the list of the squares between the two coordinates.

    We assume it's a row, a column or a diagonal.
    """
    
    assert(s_x == d_x or s_y == d_y or abs(float((d_y - s_y))/(d_x - s_x)) ==
                                                                            1.)
    i, j = cmp(d_x - s_x, 0), cmp(d_y - s_y, 0)

    p = []
    s_x, s_y = s_x + i, s_y + j
    while((s_x, s_y) != (d_x, d_y)):
        p.append((s_x, s_y))
        s_x, s_y = s_x + i, s_y + j
    
    return p

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
        self.dict_ = new_board(self, history)

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
            if(p.get_type() == KING and p.color == color):
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
        """Return the list of 'color' pieces position which control the
        coordinates (x, y)."""
        
        l = []

        # Is it controlled by a pawn?
        for i in [-1, 1]:
            pos = (x + i, y - Pawn(color).get_direction())
            if(pos in self.dict_ and self.dict_[pos].color == color and
               self.dict_[pos].get_type() == PAWN):
                   l.append(pos)
                   
        # Is it controlled by a knight?
        for (i, j) in KNIGHT_MOVES:
            pos = (x + i, y +j)
            if(pos in self.dict_ and self.dict_[pos].color == color and
               self.dict_[pos].get_type() == KNIGHT):
                   l.append(pos)
            
        # Is it controlled by a bishop/queen?
        for (i, j) in FOUR_DIAGONALS:
            tmp_x, tmp_y = x + i, y + j
            while((tmp_x, tmp_y) not in self.dict_):
                tmp_x, tmp_y = tmp_x + i, tmp_y + j
                if(tmp_x not in range(1, BOARD_SIZE+1) or
                   tmp_y not in range(1, BOARD_SIZE+1)):
                    break
            else:
                if(self.dict_[tmp_x, tmp_y].color == color and
                   self.dict_[tmp_x, tmp_y].get_type() in [BISHOP, QUEEN]):
                       l.append((tmp_x, tmp_y))
        
        # Is it controlled by a rook/queen?
        for (i, j) in CARDINAL_DIRECTION:
            tmp_x, tmp_y = x + i, y + j
            while((tmp_x, tmp_y) not in self.dict_):
                tmp_x, tmp_y = tmp_x + i, tmp_y + j
                if(tmp_x not in range(1, BOARD_SIZE+1) or
                   tmp_y not in range(1, BOARD_SIZE+1)):
                    break
            else:
                if(self.dict_[tmp_x, tmp_y].color == color and
                   self.dict_[tmp_x, tmp_y].get_type() in [ROOK, QUEEN]):
                       l.append((tmp_x, tmp_y))
                       
        # Is it controlled by a king?
        for (i, j) in CARDINAL_DIRECTION + FOUR_DIAGONALS:
            pos = (x + i, y + j)
            if(pos in self.dict_ and self.dict_[pos].color == color and
               self.dict_[pos].get_type() == KING):
                   l.append(pos)

        return l
        
    def is_check(self, color):
        """Return True if the 'color' king is in check."""

        if(self.who_controls(self.where_is_king(color), enemy_color(color))):
            return True
        else:
            return False

    def is_check_mate(self, color):
        """Return True if the 'color' king is check mate.

        It is assumed that the king is already in check.
        """

        x, y = self.where_is_king(color)
        l = self.who_controls((x, y), enemy_color(color))
        assert(len(l) != 0)
        
        # Can the king move?
        for (i, j) in FOUR_DIAGONALS + CARDINAL_DIRECTION:
            if(x + i in range(1, BOARD_SIZE + 1) and
               y + j in range(1, BOARD_SIZE + 1) and
               ((x + i, y + j) not in self.dict_ or
               self.dict_[x + i, y + j].color == enemy_color(color)) and
               not self.who_controls((x + i, y + j), enemy_color(color))):
                return False

        if(len(l) >= 2):
            return True
            
        # Can the player capture the threatening piece?
        e_x, e_y = l[0]
        l = self.who_controls((e_x, e_y), color)
        for (i, j) in l:
            if(self.dict_[i, j].can_move((i, j), (e_x, e_y))):
                return False

        # Can the player block the check?
        if(self.dict_[e_x, e_y].get_type() == KNIGHT):
            return True
        for (i, j) in get_path((x, y), (e_x, e_y)):
            l = self.who_controls((i, j), color)
            for (p_x, p_y) in l:
                if(self.dict_[p_x, p_y].can_move((p_x, p_y), (i, j))):
                    return False
        return True

    def is_pat(self, color):
        """Return True if 'color' can't play any moves."""

        row = col = range(1, BOARD_SIZE + 1)
        # NAIF METHOD, should be fix !
        for (x, y), p in self.dict_.iteritems():
            if(p.color == color):
                l = [(i, j) for i in row for j in col if i != x or j != y]
                for (i, j) in l:
                    if(p.can_move((x, y), (i, j))):
                        return False

        return True
        
    def promote(self, (x, y), type_):
        """Transform the pawn at (x, y) into type_.

        type_ must be different of PAWN.
        """

        assert((x, y) in self.dict_ and self.dict_[x, y].get_type() == PAWN and
               type_ in [KNIGHT, BISHOP, ROOK, QUEEN])

        c, h = self.dict_[x, y].color, self.dict_[x, y].history
        self.dict_[x, y] = Piece(type_, c, self.dict_, h).create()


class Piece():
    """The class Piece should only be used to create a piece.

    It give to all pieces the get_type(), is_pined() and
    let_king_under_attack() methods.
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

    def get_type(self):
        """Return the type of the piece."""
        
        return self.type_

    def is_pined(self, (x, y)):
        """Return True if the piece at (x, y) can't move because it protects
        the king from being attacked."""

        tmp = self.board[x, y]
        c, e_c = tmp.color, enemy_color(tmp.color)
        (k_x, k_y) = self.board.where_is_king(c)
        l = self.board.who_controls((k_x, k_y), e_c)

        del self.board[x, y]
        l_2 = self.board.who_controls((k_x, k_y), e_c)

        self.board[x, y] = tmp
        return len(l_2) > len(l)

    def let_king_under_attack(self, (s_x, s_y), (d_x, d_y)):
        """Return True if the piece at (s_x, s_y) can't move at (d_x, d_y)
        because it will let his king in check position."""

        assert((s_x, s_y) in self.board)

        c = self.board[s_x, s_y].color
        e_c = enemy_color(c)
        l = self.board.who_controls(self.board.where_is_king(c), e_c)          

        if(len(l) >= 2):
            return True

        if(len(l) == 1):
            if((d_x, d_y) == l[0] and not self.board[s_x, s_y].is_pined((s_x,
                                                                        s_y))):
                return False
            else:
                return True

        if(not self.board[s_x, s_y].is_pined((s_x, s_y))):
            return False
        else:   # Search for the position of the piece who pins (s_x, s_y)
            tmp = self.board[s_x, s_y]
            del self.board[s_x, s_y]
            
            l = self.board.who_controls(self.board.where_is_king(c), e_c)
            self.board[s_x, s_y] = tmp
            assert(len(l) == 1)

            if(l[0] == (d_x, d_y)):
                return False
            else:
                return True
                

class Pawn(Piece):
    """The class Pawn represents a pawn in chess game.

    A pawn can move forward one square, if that square is unoccupied. If it
    has not yet moved, each pawn has the option of moving two squares forward
    provided both squares in front of the pawn are unoccupied.
    A pawn cannot move backwards.
    Pawns are the only pieces that capture differently from how they move.
    They can capture an enemy piece on either of the two squares diagonally in
    front of them but cannot move to these spaces if they are vacant.
    Pawn have two special moves: promotion and 'en passant'.
    """

    def __init__(self, color, board={}, history=[]):
        self.color = color
        self.board = board
        self.history = history
        self.type_ = PAWN

    def get_direction(self):
        """Return the pawn direction depending on his color."""
        
        if(self.color == WHITE_COLOR):
            return WHITE_PAWN_DIRECTION
        if(self.color == BLACK_COLOR):
            return BLACK_PAWN_DIRECTION
        sys.exit("Unknown color while looking for the direction of the pawn")

    def get_initial_row(self):
        """Return the initial row of the pawn."""

        if(self.color == WHITE_COLOR):
            return WHITE_PAWN_ROW
        if(self.color == BLACK_COLOR):
            return BLACK_PAWN_ROW
        sys.exit("Unknown color while looking for the initial row of pawns")

    def get_promotion_row(self):
        """Return the promotion row of the pawn"""

        if(self.color == WHITE_COLOR):
            return BOARD_SIZE
        if(self.color == BLACK_COLOR):
            return 1
        sys.exit("Unknown color while looking for the promotion row of pawns")

    def can_move(self, (s_x, s_y), (d_x, d_y)):
        """Say if the pawn at (s_x, s_y) can go to (d_x, d_y).

        Pawn have two special moves called 'en passant' and promotion.
        Return the Move if the pawn can, else return None.
        """
        
        assert(self.board[s_x, s_y].get_type() == self.type_ and
               self.board[s_x, s_y].color == self.color and
               s_x in range(1, BOARD_SIZE + 1) and
               s_y in range(1, BOARD_SIZE + 1) and
               d_x in range(1, BOARD_SIZE + 1) and
               d_y in range(1, BOARD_SIZE + 1) and
               (s_x, s_y) != (d_x, d_y))
        if(self.let_king_under_attack((s_x, s_y), (d_x, d_y))):
            return None
        
        d = self.get_direction()

        # Pawn moves two squares forward
        if(s_x == d_x and (d_y - s_y) ==  2 * d and
           s_y == self.get_initial_row()):
            if (d_x, d_y) not in self.board and (d_x, d_y-d) not in self.board:
                return Move((s_x, s_y), (d_x, d_y), NORMAL_MOVE)
            else:
                return None

        # Pawn moves one square forward
        if(s_x == d_x and (d_y - s_y) ==  d and (d_x, d_y) not in self.board):
            if(d_y == self.get_promotion_row()):
                return Move((s_x, s_y), (d_x, d_y), PROMOTION)
            else:
                return Move((s_x, s_y), (d_x, d_y), NORMAL_MOVE)

        # Pawn moves one square diagonally
        if(abs(s_x - d_x) == 1 and (d_y - s_y) ==  d):
            if((d_x, d_y) in self.board and self.board[d_x, d_y].color ==
                                                      enemy_color(self.color)):
                if(d_y == self.get_promotion_row()):
                    return Move((s_x, s_y), (d_x, d_y), CAPTURE_PROMOTION)
                else:
                    return Move((s_x, s_y), (d_x, d_y), CAPTURE)
            if((d_x, d_y) not in self.board and self.history[-1] ==
               Move((d_x, d_y + d), (d_x, d_y - d), NORMAL_MOVE)):
                return Move((s_x, s_y), (d_x, d_y), EN_PASSANT)
            else:
                return None
        return None

class Bishop(Piece):
    """The class Bishop represents a bishop in chess Game.

    The bishop moves any number of vacant squares in any diagonal direction.
    """

    def __init__(self, color, board):
        self.color = color
        self.board = board
        self.type_ = BISHOP

    def can_move(self, (s_x, s_y), (d_x, d_y)):
        """Say if the bishop at (s_x, s_y) can go to (d_x, d_y).

        Return the Move if the bishop can, else return None.
        """

        assert(self.board[s_x, s_y].get_type() == self.type_ and
               self.board[s_x, s_y].color == self.color and
               s_x in range(1, BOARD_SIZE + 1) and
               s_y in range(1, BOARD_SIZE + 1) and
               d_x in range(1, BOARD_SIZE + 1) and
               d_y in range(1, BOARD_SIZE + 1) and
               (s_x, s_y) != (d_x, d_y))
        if(self.let_king_under_attack((s_x, s_y), (d_x, d_y))):
            return None

        if(d_x == s_x or abs(float((d_y - s_y))/(d_x - s_x)) != 1.):
            return None

        for (i, j) in get_path((s_x, s_y), (d_x, d_y)):
            if((i, j) in self.board):
                return None

        if((d_x, d_y) not in self.board):
            return Move((s_x, s_y), (d_x, d_y), NORMAL_MOVE)

        if(self.board[d_x, d_y].color == enemy_color(self.color)):
            return Move((s_x, s_y), (d_x, d_y), CAPTURE)

        return None
            
        
class Knight(Piece):
    """The class Knight represents a knight in chess game.

    The knight moves two squares horizontally then one square vertically, or
    one square horizontally then two squares vertically. Its move is not
    blocked by other pieces: it jumps to the new location.
    """

    def __init__(self, color, board):
        self.color = color
        self.board = board
        self.type_ = KNIGHT

    def can_move(self, (s_x, s_y), (d_x, d_y)):
        """Say if the knight at (s_x, s_y) can go to (d_x, d_y).

        Return the Move if the knight can, else return None.
        """

        assert(self.board[s_x, s_y].get_type() == self.type_ and
               self.board[s_x, s_y].color == self.color and
               s_x in range(1, BOARD_SIZE + 1) and
               s_y in range(1, BOARD_SIZE + 1) and
               d_x in range(1, BOARD_SIZE + 1) and
               d_y in range(1, BOARD_SIZE + 1) and
               (s_x, s_y) != (d_x, d_y))
        if(self.let_king_under_attack((s_x, s_y), (d_x, d_y))):
            return None

        if((d_x, d_y) not in self.board):
            return Move((s_x, s_y), (d_x, d_y), NORMAL_MOVE)
        if(self.board[d_x, d_y].color == enemy_color(self.color)):
            return Move((s_x, s_y), (d_x, d_y), CAPTURE)
            
        return None

class Rook(Piece):
    """The class Rook represents a rook in chess game.
    The rook moves any number of vacant squares vertically or horizontally.
    Rook have a special move shared with the king called castling.
    """

    def __init__(self, color, board, history):
        self.color = color
        self.board = board
        self.history = history
        self.type_ = ROOK

    def castling(self, (x, y)):
        """Move the king to perform a castling while the rook is at (x, y).

        It assumes that the player can castling.
        """

        assert(y in [1, BOARD_SIZE] and (x, y) in self.board and
               self.board[x, y].get_type() == ROOK and
               self.board[x, y].color == self.color and
               x in [KINGSIDE_ROOK_POS_X, QUEENSIDE_ROOK_POS_X])

        k_pos = King(self.color).get_initial_pos()
        assert(k_pos in self.board)
               
        if(x == KINGSIDE_ROOK_POS_X):
            self.board[KINGSIDE_KING_POS_X, y] = self.board[k_pos]
            del self.board[k_pos]

        if(x == QUEENSIDE_ROOK_POS_X):
            self.board[QUEENSIDE_KING_POS_X, y] = self.board[k_pos]
            del self.board[k_pos]

    def can_castling(self, (s_x, s_y), (d_x, d_y)):
        """Return True if the rook can castling.

        It uses the can_castling() method of the king.
        """

        if(self.color == WHITE_COLOR):
            x, y = WHITE_KING_POS
        elif(self.color == BLACK_COLOR):
            x, y = BLACK_KING_POS
        else:
            sys.exit("Unknown color while looking for if the rook can castle")

        if((x, y) not in self.board or self.board[x, y].get_type() != KING or
           self.board[x, y].color != self.color):
            return False

        if(d_x == KINGSIDE_ROOK_POS_X and d_y == y):
            return self.board[x, y].can_castling((x, y), (KINGSIDE_KING_POS_X,
                                                                          d_y))
        if(d_x == QUEENSIDE_ROOK_POS_X and d_y == y):
            return self.board[x, y].can_castling((x, y), (QUEENSIDE_KING_POS_X,
                                                                          d_y))
        return False
        
    def can_move(self, (s_x, s_y), (d_x, d_y)):
        """Say if the rook at (s_x, s_y) can go to (d_x, d_y).

        Return the Move if the rook can, else return None.
        """

        assert(self.board[s_x, s_y].get_type() == self.type_ and
               self.board[s_x, s_y].color == self.color and
               s_x in range(1, BOARD_SIZE + 1) and
               s_y in range(1, BOARD_SIZE + 1) and
               d_x in range(1, BOARD_SIZE + 1) and
               d_y in range(1, BOARD_SIZE + 1) and
               (s_x, s_y) != (d_x, d_y))
        if(self.let_king_under_attack((s_x, s_y), (d_x, d_y))):
            return None

        if(s_x != d_x and s_y != d_y):
            return None

        if(self.can_castling((s_x, s_y), (d_x, d_y))):
            return Move((s_x, s_y), (d_x, d_y), CASTLING)
            
        for (i, j) in get_path((s_x, s_y), (d_x, d_y)):
            if((i, j) in self.board):
                return None

        if((d_x, d_y) not in self.board):
            return Move((s_x, s_y), (d_x, d_y), NORMAL_MOVE)

        if(self.board[d_x, d_y].color == enemy_color(self.color)):
            return Move((s_x, s_y), (d_x, d_y), CAPTURE)

        return None

class Queen(Piece):
    """The class Queen represents a queen in chess game.

    The queen can move any number of vacant squares diagonally, horizontally,
    or vertically.
    """
    
    def __init__(self, color, board):
        self.color = color
        self.board = board
        self.type_ = QUEEN
        
    def can_move(self, (s_x, s_y), (d_x, d_y)):
        """Say if the queen at (s_x, s_y) can go to (d_x, d_y).

        Return the Move if the queen can, else return None.
        """

        assert(self.board[s_x, s_y].get_type() == self.type_ and
               self.board[s_x, s_y].color == self.color and
               s_x in range(1, BOARD_SIZE + 1) and
               s_y in range(1, BOARD_SIZE + 1) and
               d_x in range(1, BOARD_SIZE + 1) and
               d_y in range(1, BOARD_SIZE + 1) and
               (s_x, s_y) != (d_x, d_y))
        if(self.let_king_under_attack((s_x, s_y), (d_x, d_y))):
            return None

        if(s_x != d_x and s_y != d_y and abs(float((d_y - s_y))/(d_x - s_x)) !=
                                                                           1.):

            return None

        for (i, j) in get_path((s_x, s_y), (d_x, d_y)):
            if((i, j) in self.board):
                return None

        if((d_x, d_y) not in self.board):
            return Move((s_x, s_y), (d_x, d_y), NORMAL_MOVE)

        if(self.board[d_x, d_y].color == enemy_color(self.color)):
            return Move((s_x, s_y), (d_x, d_y), CAPTURE)

        return None

               
class King(Piece):
    """The class King represents a king in chess game.

    The king can move exactly one square horizontally, vertically, or
    diagonally.
    The king have a special move shared with the rook called castling.
    """
    
    def __init__(self, color, board={}, history=[]):
        self.color = color
        self.board = board
        self.history = history
        self.type_ = KING

    def castling(self, (x, y)):
        """Move the rook to perform a castling while the king is at (x, y).

        It is assumed that the player can castling.
        """

        assert(y in [1, BOARD_SIZE] and (x, y) in self.board and
               self.board[x, y].get_type() == KING and
               self.board[x, y].color == self.color and
               x in [KINGSIDE_KING_POS_X, QUEENSIDE_KING_POS_X])

        if(x == KINGSIDE_KING_POS_X):
            assert((BOARD_SIZE, y) in self.board and
                   (KINGSIDE_ROOK_POS_X, y) not in self.board)
            
            self.board[KINGSIDE_ROOK_POS_X, y] = self.board[BOARD_SIZE, y]
            del self.board[BOARD_SIZE, y]

        if(x == QUEENSIDE_KING_POS_X):
            assert((1, y) in self.board and
                   (QUEENSIDE_ROOK_POS_X, y) not in self.board)
            
            self.board[QUEENSIDE_ROOK_POS_X, y] = self.board[1, y]
            del self.board[1, y]

    def get_initial_pos(self):
        """Return the initial coordinate of the king."""
        if(self.color == WHITE_COLOR):
            return WHITE_KING_POS
        if(self.color == BLACK_COLOR):
            return BLACK_KING_POS
        sys.exit("Unknown color while looking for the initial king position")

    def can_castling(self, (s_x, s_y), (d_x, d_y)):
        """Return True if the king can castling."""

        if(abs(s_x - d_x) != 2 or s_y != d_y or self.board.is_check(self.color)
           or (s_x, s_y) != self.get_initial_pos()):
            return False

        # Get the coordinate of the rook
        y = d_y
        if(d_x == KINGSIDE_KING_POS_X):
            x = 1
        elif(d_x == QUEENSIDE_KING_POS_X):
            x = BOARD_SIZE
        else:
            sys.exit("Unknown castling move")
        if((x, y) not in self.board or self.board[x, y].get_type() != ROOK or
           self.board[x, y].color != self.color):
            return False
        
        # Did the king or the rook move?
        for m in self.history:
            if(m.src == ((x, y) or (s_x, s_y))):
                return False

        # Are the squares that the king will pass through, empty and not under
        # enemy control?
        for (i, j) in get_path((s_x, s_y), (d_x, d_y)) + [(d_x, d_y)]:
            if((i, j) in self.board or self.board.who_controls((i, j),
                                                     enemy_color(self.color))):
                return False

        return True
        
    def can_move(self, (s_x, s_y), (d_x, d_y)):
        """Say if the king at (s_x, s_y) can go to (d_x, d_y).

        Return the Move if the king can, else return None.
        """

        assert(self.board[s_x, s_y].get_type() == self.type_ and
               self.board[s_x, s_y].color == self.color and
               s_x in range(1, BOARD_SIZE + 1) and
               s_y in range(1, BOARD_SIZE + 1) and
               d_x in range(1, BOARD_SIZE + 1) and
               d_y in range(1, BOARD_SIZE + 1) and
               (s_x, s_y) != (d_x, d_y))

        if(self.can_castling((s_x, s_y), (d_x, d_y))):
            return Move((s_x, s_y), (d_x, d_y), CASTLING)

        if(abs(s_x - d_x) > 1 or abs(s_y - d_y) > 1):
            return None

        if(self.board.who_controls((d_x, d_y), enemy_color(self.color))):
            return None

        if((d_x, d_y) not in self.board):
            return Move((s_x, s_y), (d_x, d_y), NORMAL_MOVE)
        if(self.board[d_x, d_y].color == enemy_color(self.color)):
            return Move((s_x, s_y), (d_x, d_y), CAPTURE)

        return None

        