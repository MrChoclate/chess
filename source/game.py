"""Game module

This module contains the class Game which allow you to play chess.
He use the module rules to work and to know if everything is valid or not.
"""

import rules as ru

"""Constants"""
BOARD_SIZE = 8

(   # Color
WHITE_COLOR,
BLACK_COLOR
) = range(2)

(   # Move type
NORMAL_MOVE,
CAPTURE,
CASTLING,
EN_PASSANT,
PROMOTION,
CAPTURE_PROMOTION
) = range(6)

(   # This is what the move method can return.
INVALID_MOVE,
VALID_MOVE,
PROMOTE,
CHECK,
CHECK_MATE
) = range(4)

class Player():
    """The class player is used to know data about the player.

    It's used to know the list of captured pieces, the time spent playing, and
    if the player is actually playing.
    """

    def __init__(self, color):
        self.color = color
        self.captured_pieces = []
        self.time_spent = 0
        if(color == WHITE_COLOR):
            self.playing = True
        elif(color == BLACK_COLOR):
            self.playing = False
        else:
            sys.exit("Unknown color while initializing the player");

    def is_playing(self):
        """Return True if the player is playing."""

        return self.playing

    def played(self):
        """The player played and is now not playing."""

        self.playing = False

    def must_play(self):
        """The player is now playing."""

        self.playing = True

    def get_captured_pieces(self):
        """Return the list of captured pieces by the player"""

        return self.captured_pieces

class Game:
    """The class Game contains all the mecanism to play chess."""

    def __init__(self):
        """Create the board, the player and initialize the history."""

        self.history = []
        self.undo_history = []
        self.board = ru.Board(self.history);
        self.white_player = Player(WHITE_COLOR)
        self.black_player = Player(BLACK_COLOR)

    def __get_player(self, color):
        """Return the 'color' player attribute."""

        if(color == WHITE_COLOR):
            return white_player
        if(color == BLACK_COLOR):
            return black_player
        sys.exit("Unknown color while looking for the player attribute")
        
    def get_board(self):
        """Return the board."""
        
        return self.board.dict_

    def undo(self):
        """Undo the last Move and store it in undo_history."""

    def redo(self):
        """Redo the last undone Move."""

    def move(self, color, (src_x, src_y), (dest_x, dest_y)):
        """Move the 'color' piece from (src_x, src_y) to (dest_x, dest_y).

        If the move or the parameters are invalid, it return INVALID_MOVE.
        If the move is valid, it can return:
        VALID_MOVE if the piece moved.
        PROMOTE if there is a pawn to promote.
        CHECK if now the ennemy of 'color' is in check.
        CHECK mate if 'color' won the game.
        """

        # Wrongs parameters
        if(color not in [WHITE_COLOR, BLACK_COLOR] or (src_x, src_y) ==
           (dest_x, dest_y) or (src_x and src_y and dest_x and dest_y) not in
           range(1, BOARD_SIZE+1) or (src_x, src_y) not in self.board or
           self.board[src_x, src_y].color != color):
            return INVALID_MOVE

            
        m = self.board[src_x, src_y].can_move((src_x, src_y), (dest_x, dest_y))

        if(type(m) == bool and m == False):
            return INVALID_MOVE
        assert(type(m) == type(ru.Move))

        self.history.append(m)

        if(m.type_ == (CAPTURE or CAPTURE_PROMOTION)):
            self.__get_player(color).captured_pieces.append(self.board[dest_x,
                                                                       dest_y])
        if(m.type_ == EN_PASSANT):
            del self.board[dest_x, dest_y - ru.Pawn(color).get_direction()]
                                                                  
        self.board[dest_x, dest_y] = self.board[src_x, src_y]
        del self.board[src_x, src_y]

        if(m.type_ == CASTLING):
            board[src_x, src_y].castling((src_x, src_y))

            
        if(m.type_ == (PROMOTION or CAPTURE_PROMOTION)):
            return PROMOTE

        if(self.board.is_check(ru.enemy_color(color))):
            if(self.board.is_check_mate(ru.enemy_color(color)):
                return CHECK_MATE
            return CHECK

        return VALID_MOVE
        