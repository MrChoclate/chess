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
) = range(5)

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

class Game():
    """The class Game contains all the mecanism to play chess."""

    def __init__(self):
        """Create the board, the player and initialize the history."""

        self.history = []
        self.undo_history = []
        self.undo_promotion_history = []
        self.board = ru.Board(self.history);
        self.white_player = Player(WHITE_COLOR)
        self.black_player = Player(BLACK_COLOR)

    def __get_player(self, color):
        """Return the 'color' player attribute."""

        if(color == WHITE_COLOR):
            return self.white_player
        if(color == BLACK_COLOR):
            return self.black_player
        sys.exit("Unknown color while looking for the player attribute")
        
    def get_board(self):
        """Return the board."""
        
        return self.board.dict_

    def undo(self):
        """Undo the last Move and store it in undo_history."""

        if(len(self.history) == 0):
            return None # You can't undo if you didn't play.
        
        src, dest, t = self.history[-1]
        self.undo_history.append(self.history.pop())
        c = self.board[dest].color

        assert(dest in self.board and src not in self.board)
        self.board[src] = self.board[dest]
        del self.board[dest]

        if(t in [CAPTURE, CAPTURE_PROMOTION, EN_PASSANT]):
            assert(len(self.__get_player(c).captured_pieces) != 0)
            if(t == EN_PASSANT):
                x, y = dest
                y -= ru.Pawn(c).get_direction()
                dest = (x, y)
            self.board[dest] = self.__get_player(c).captured_pieces.pop()

        if(t in [PROMOTION, CAPTURE_PROMOTION]):
            self.undo_promotion_history.append(self.board[src])
            self.board[src] = Pawn(c, self.board, self.history)

        if(t == CASTLING): # There is a second piece to move, which moved from
            x, y = dest    # the src to the dest which are calculated here.
            if(x == ru.KINGSIDE_KING_POS_X):
                dest = (x - 1, y)
                src = (BOARD_SIZE, y)
            elif(x == ru.QUEENSIDE_KING_POS_X):
                dest = (x + 1, y)
                src = (1, y)
            elif(x == ru.KINGSIDE_ROOK_POS_X):
                dest = (x + 1, y)
                src = ru.King(c).get_initial_pos()
            elif(x == ru.QUEENSIDE_ROOK_POS_X):
                dest = (x - 1, y)
                src = ru.King(c).get_initial_pos()
            else:
                sys.exit("Unknown x position while undo a castling")

            assert(dest in self.board)
            self.board[src] = self.board[dest]
            del self.board[dest]

        self.__get_player(c).must_play()
        self.__get_player(ru.enemy_color(c)).played()

    def redo(self):
        """Redo the last undone Move."""

        if(len(self.undo_history) == 0):
            return None

        src, dest, t = self.undo_history[-1]

        m_type = self.move(self.board[src].color, src, dest, player_move=False)
        self.history.append(self.undo_history.pop())
        assert(m_type != INVALID_MOVE)
        if(t in [PROMOTION, CAPTURE_PROMOTION]):
            self.board[dest] = self.undo_promotion_history.pop()
        
    def move(self, color, (src_x, src_y), (dest_x, dest_y), player_move=True):
        """Move the 'color' piece from (src_x, src_y) to (dest_x, dest_y).

        The player_move parameter is use to know if the move is play by a
        player or if it's an automatic move of the redo method.
        
        If the move or the parameters are invalid, it return INVALID_MOVE.
        If the move is valid, it can return:
        VALID_MOVE if the piece moved.
        PROMOTE if there is a pawn to promote.
        CHECK if now the ennemy of 'color' is in check.
        CHECK mate if 'color' won the game.
        """

        # Wrongs parameters
        if(not self.__get_player(color).is_playing() or
           color not in [WHITE_COLOR, BLACK_COLOR] or (src_x, src_y) ==
           (dest_x, dest_y) or src_x not in range(1, BOARD_SIZE+1) or
           src_y not in range(1, BOARD_SIZE+1) or
           dest_x not in range(1, BOARD_SIZE+1) or
           dest_y not in range(1, BOARD_SIZE+1) or
           (src_x, src_y) not in self.board or
           self.board[src_x, src_y].color != color):
            return INVALID_MOVE

            
        m = self.board[src_x, src_y].can_move((src_x, src_y), (dest_x, dest_y))

        if(type(m) == bool and m == False):
            return INVALID_MOVE
        assert(type(m) == ru.Move)

        self.history.append(m)

        if(m.type_ in [CAPTURE, CAPTURE_PROMOTION]):
            self.__get_player(color).captured_pieces.append(self.board[dest_x,
                                                                       dest_y])
        if(m.type_ == EN_PASSANT):
            y = dest_y - ru.Pawn(color).get_direction()
            self.__get_player(color).captured_pieces.append(self.board[dest_x,
                                                                            y])
            del self.board[dest_x,y]
                                                                  
        self.board[dest_x, dest_y] = self.board[src_x, src_y]
        del self.board[src_x, src_y]

        if(m.type_ == CASTLING):
            self.board[dest_x, dest_y].castling((dest_x, dest_y))


        self.__get_player(color).played()
        self.__get_player(ru.enemy_color(color)).must_play()

        if(player_move):            # This is for not clear the history while
            self.undo_history = []  # using the redo method.
            self.undo_promotion_history = []
        
        if(m.type_ in [PROMOTION, CAPTURE_PROMOTION]):
            return PROMOTE

        if(self.board.is_check(ru.enemy_color(color))):
            if(self.board.is_check_mate(ru.enemy_color(color))):
                self.__get_player(ru.enemy_color(color)).played()
                return CHECK_MATE
            return CHECK

        return VALID_MOVE

    def promote(self, (x, y), type_):
        """Transform the pawn at (x, y) into type_.

        type_ must be different of PAWN.
        """

        self.board.promote((x, y), type_)
