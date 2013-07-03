"""Unittest of the module game.py.

For now, the main goal is to play several games."""

from collections import namedtuple
import unittest
import game

"""Constants"""
W = game.WHITE_COLOR
B = game.BLACK_COLOR

I = game.INVALID_MOVE
V = game.VALID_MOVE
P = game.PROMOTE
C = game.CHECK
M = game.CHECK_MATE

Move = namedtuple('Move', 'src, dest, type_')

class PlayRecordedGames(unittest.TestCase):
    """Test playing severals games."""
    
    def setUp(self):
        self.g = game.Game()

    def verify_undo_redo(self):
        """Undo all moves and check if the board is the initial board. Then
        redo all moves and check if it's still the same."""

        save = self.g.get_board().copy()
        for i in xrange(100):
            self.g.undo()
        # Verify the undo method.
        b_ini = game.Game().get_board()
        b = self.g.get_board()
        for key, value in b_ini.iteritems():
            self.assertIn(key, b)
            self.assertEqual(value.color, b[key].color)
            self.assertEqual(value.get_type(), b[key].get_type())

        # Verify the redo method.
        for i in xrange(100):
            self.g.redo()
        self.assertEqual(self.g.get_board(), save)
        
    def tearDown(self):
        self.verify_undo_redo()

    def play_game(self, moves):
        """Test the list of moves in the list 'moves'.

        A move is a namedtuple which have three attributes:
        src, dest and type_.
        type_ is what the Game.move() method should return.
        """
        
        c = W

        for m in moves:
             self.assertEqual(self.g.move(c, m.src, m.dest), m.type_)
             if(c == W):
                 c = B
             else:
                 c = W

    def test_game_1(self):
        """Garry Kasparov vs Veselin Topalov - Wijk aan Zee (Netherlands) 1999
        "Kasparov's Immortal"

        1. e4 d6 2. d4 Nf6 3. Nc3 g6 4. Be3 Bg7 5. Qd2 c6 6. f3 b5 7. Nge2 Nbd7
        8. Bh6 Bxh6 9. Qxh6 Bb7 10. a3 e5 11. O-O-O Qe7 12. Kb1 a6
        13. Nc1 O-O-O 14. Nb3 exd4 15. Rxd4 c5 16. Rd1 Nb6 17. g3 Kb8
        18. Na5 Ba8 19. Bh3 d5 20. Qf4+ K 7 21. Rhe1 d4 22. Nd5 Nbxd5
        23. exd5 Qd6 24. Rxd4 cxd4 25. R7+ Kb6 26. Qxd4+ Kxa5 27. b4+ Ka4
        28. Qc3 Qxd5  29. Ra7 Bb7 30.Rxb7 Qc4 31. Qxf6 Kxa3 32. Qxa6+ xb4
        33. c3+ Kxc3 34. Qa1+ Kd 35. Qb2+ Kd1 3 6. Bf1 Rd2 37 Rd7 Rxd7
        38. Bxc4 bxc4 9. Qxh8 Rd3 40. Qa8 c3 41. Qa4+ Ke1 42. f f5
        43. Kc1 Rd2 44. Qa7
        """

        moves = [] # ! Xer ! This is what you should fill.
                   # You should also create new tests like test_game_2 from
                   # http://www.365chess.com/
                   # Be aware that our mat notation is ++
         
        self.play_game(moves)

    def test_game_2(self):
        """Scholar's mate.

        1. e4 e5 2. Bc4 Nc6 3. Qh5 Nf6 4. Qxf7++
        """

        moves = [Move((5, 2), (5, 4), V), Move((5, 7), (5, 5), V),
                 Move((6, 1), (3, 4), V), Move((2, 8), (3, 6), V),
                 Move((4, 1), (8, 5), V), Move((7, 8), (6, 6), V),
                 Move((8, 5), (6, 7), M)]

        self.play_game(moves)

    def test_en_passant(self):
        """'en passant' rule."""

        self.assertEqual(self.g.move(W, (1, 2), (1, 4)), V) # 1. a4
        self.assertEqual(self.g.move(B, (1, 7), (1, 6)), V) #       a6

        self.assertEqual(self.g.move(W, (1, 4), (1, 5)), V) # 2. a5
        self.assertEqual(self.g.move(B, (2, 7), (2, 5)), V) #       b5

        self.assertEqual(self.g.move(W, (1, 5), (2, 6)), V) # 3. axb6
        self.assertNotIn((2, 5), self.g.board) # The piece has been taken

        

if __name__ == '__main__':
    unittest.main()
    