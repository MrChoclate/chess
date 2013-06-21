"""Unittest of the module game.py.

For now, the main goal is to play several games."""

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

class PlayRecordedGames(unittest.TestCase):

    def setUp(self):
        self.g = game.Game()

    def test_game_1(self):
        """Garry Kasparov vs Veselin Topalov - Wijk aan Zee (Netherlands) 1999
        "Kasparov's Immortal"
        """

        self.assertEqual(self.g.move(W, (5, 2), (5, 4)), V) # 1. e4
        self.assertEqual(self.g.move(B, (4, 7), (4, 6)), V) #       d6

        self.assertEqual(self.g.move(W, (4, 2), (4, 4)), V) # 2. d4
        self.assertEqual(self.g.move(B, (7, 8), (6, 6)), V) #       Nf6

        self.assertEqual(self.g.move(W, (2, 1), (3, 3)), V) # 3. Nc3
        self.assertEqual(self.g.move(B, (7, 7), (7, 6)), V) #         g6

        self.assertEqual(self.g.move(W, (3, 1), (5, 3)), V) # 4. Be3
        self.assertEqual(self.g.move(B, (6, 8), (7, 7)), V) #         Bg7

        self.assertEqual(self.g.move(W, (4, 1), (4, 2)), V) # 5. Qd2
        self.assertEqual(self.g.move(B, (3, 7), (3, 6)), V) #        c6

        self.assertEqual(self.g.move(W, (6, 2), (6, 3)), V) # 6. f3
        self.assertEqual(self.g.move(B, (2, 7), (2, 5)), V) #       b5

        self.assertEqual(self.g.move(W, (7, 1), (5, 2)), V) # 7. Nge2
        self.assertEqual(self.g.move(B, (2, 8), (4, 7)), V) #         Nbd7

        self.assertEqual(self.g.move(W, (5, 3), (8, 6)), V) # 8. Bh6
        self.assertEqual(self.g.move(B, (7, 7), (8, 6)), V) #         Bxh6

        self.assertEqual(self.g.move(W, (4, 2), (8, 6)), V) # 9. Qxh6
        self.assertEqual(self.g.move(B, (3, 8), (2, 7)), V) #         Bb7

        self.assertEqual(self.g.move(W, (1, 2), (1, 3)), V) # 10. a3
        self.assertEqual(self.g.move(B, (5, 7), (5, 5)), V) #        e5

        self.assertEqual(self.g.move(W, (5, 1), (3, 1)), V) # 11. O-O-O
        self.assertEqual(self.g.move(B, (4, 8), (5, 7)), V) #           Qe7

        self.assertEqual(self.g.move(W, (3, 1), (2, 1)), V) # 12. Kb1
        self.assertEqual(self.g.move(B, (1, 7), (1, 6)), V) #         a6

        self.assertEqual(self.g.move(W, (5, 2), (3, 1)), V) # 13. Nc1
        self.assertEqual(self.g.move(B, (1, 8), (4, 8)), V) #         O-O-O

        self.assertEqual(self.g.move(W, (3, 1), (2, 3)), V) # 14. Nb3
        self.assertEqual(self.g.move(B, (5, 5), (4, 4)), V) #         exd4

        self.assertEqual(self.g.move(W, (4, 1), (4, 4)), V) # 15. Rxd4
        self.assertEqual(self.g.move(B, (3, 6), (3, 5)), V) #          c5

        self.assertEqual(self.g.move(W, (4, 4), (4, 1)), V) # 16. Rd1
        self.assertEqual(self.g.move(B, (4, 7), (2, 6)), V) #         Nb6

        self.assertEqual(self.g.move(W, (7, 2), (7, 3)), V) # 17. g3
        self.assertEqual(self.g.move(B, (3, 8), (2, 8)), V) #        Kb8

        self.assertEqual(self.g.move(W, (2, 3), (1, 5)), V) # 18. Na5
        self.assertEqual(self.g.move(B, (2, 7), (1, 8)), V) #          Ba8

        self.assertEqual(self.g.move(W, (6, 1), (8, 3)), V) # 19. Bh3
        self.assertEqual(self.g.move(B, (4, 6), (4, 5)), V) #         d5

        self.assertEqual(self.g.move(W, (8, 6), (6, 4)), C) # 20. Qf4
        self.assertEqual(self.g.move(B, (2, 8), (1, 7)), V) #         Ka7

        self.assertEqual(self.g.move(W, (8, 1), (5, 1)), V) # 21. Rhe1
        self.assertEqual(self.g.move(B, (4, 5), (4, 4)), V) #          d4

        self.assertEqual(self.g.move(W, (3, 3), (4, 5)), V) # 22. Nd5
        self.assertEqual(self.g.move(B, (2, 6), (4, 5)), V) #         Nbxd5

        self.assertEqual(self.g.move(W, (5, 4), (4, 5)), V) # 23. exd5
        self.assertEqual(self.g.move(B, (5, 7), (4, 6)), V) #          Qd6

        self.assertEqual(self.g.move(W, (4, 1), (4, 4)), V) # 24. Rxd4
        self.assertEqual(self.g.move(B, (3, 5), (4, 4)), V) #          cxd4

        self.assertEqual(self.g.move(W, (5, 1), (5, 7)), C) # 25. Re7
        self.assertEqual(self.g.move(B, (1, 7), (2, 6)), V) #         Kb6

        self.assertEqual(self.g.move(W, (6, 4), (4, 4)), C) # 26. Qxd4
        self.assertEqual(self.g.move(B, (2, 6), (1, 5)), V) #          Kxa5

        self.assertEqual(self.g.move(W, (2, 2), (2, 4)), C) # 27. b4
        self.assertEqual(self.g.move(B, (1, 5), (1, 4)), V) #        Ka4

        self.assertEqual(self.g.move(W, (4, 4), (3, 3)), V) # 28. Qc3
        self.assertEqual(self.g.move(B, (4, 6), (4, 5)), V) #         Qxd5

        self.assertEqual(self.g.move(W, (5, 7), (1, 7)), V) # 29. Ra7
        self.assertEqual(self.g.move(B, (1, 8), (2, 7)), V) #         Bb7

        self.assertEqual(self.g.move(W, (1, 7), (2, 7)), V) # 30. Rxb7
        self.assertEqual(self.g.move(B, (4, 5), (3, 4)), V) #          Qc4

        self.assertEqual(self.g.move(W, (3, 3), (6, 6)), V) # 31. Qxf6
        self.assertEqual(self.g.move(B, (1, 4), (1, 3)), V) #          Kxa3

        self.assertEqual(self.g.move(W, (6, 6), (1, 6)), C) # 32. Qxa6
        self.assertEqual(self.g.move(B, (1, 3), (2, 4)), V) #          Kxb4

        self.assertEqual(self.g.move(W, (3, 2), (3, 3)), C) # 33. c3
        self.assertEqual(self.g.move(B, (2, 4), (3, 3)), V) #        Kxc3

        self.assertEqual(self.g.move(W, (1, 6), (1, 1)), C) # 34. Qa1
        self.assertEqual(self.g.move(B, (3, 3), (4, 2)), V) #         Kd2

        self.assertEqual(self.g.move(W, (1, 1), (2, 2)), C) # 35. Qb2
        self.assertEqual(self.g.move(B, (4, 2), (4, 1)), V) #         Kd1

        self.assertEqual(self.g.move(W, (8, 3), (6, 1)), V) # 36. Bf1
        self.assertEqual(self.g.move(B, (4, 8), (4, 2)), V) #         Rd2

        self.assertEqual(self.g.move(W, (2, 7), (4, 7)), V) # 37. Rd7
        self.assertEqual(self.g.move(B, (4, 2), (4, 7)), V) #         Rxd7

        self.assertEqual(self.g.move(W, (6, 1), (3, 4)), V) # 38. Bxc4
        self.assertEqual(self.g.move(B, (2, 5), (3, 4)), V) #          bxc4

        self.assertEqual(self.g.move(W, (2, 2), (8, 8)), V) # 39. Qxh8
        self.assertEqual(self.g.move(B, (4, 7), (4, 3)), V) #          Rd3

        self.assertEqual(self.g.move(W, (8, 8), (1, 8)), V) # 40. Qa8
        self.assertEqual(self.g.move(B, (3, 4), (3, 3)), V) #         c3

        self.assertEqual(self.g.move(W, (1, 8), (1, 4)), C) # 41. Qa4
        self.assertEqual(self.g.move(B, (4, 1), (5, 1)), V) #         Ke1

        self.assertEqual(self.g.move(W, (6, 3), (6, 4)), V) # 42.f4
        self.assertEqual(self.g.move(B, (6, 7), (6, 5)), V) #       f5

        self.assertEqual(self.g.move(W, (2, 1), (3, 1)), V) # 43. Kc1
        self.assertEqual(self.g.move(B, (4, 3), (4, 2)), V) #         Rd2

        self.assertEqual(self.g.move(W, (1, 4), (1, 6)), V) # 44. Qa6

    def test_mate(self):
        """Scholar's mate"""

        self.assertEqual(self.g.move(W, (5, 2), (5, 4)), V) # 1. e4
        self.assertEqual(self.g.move(B, (5, 7), (5, 5)), V) #       e5

        self.assertEqual(self.g.move(W, (6, 1), (3, 4)), V) # 2. Bc4
        self.assertEqual(self.g.move(B, (2, 8), (3, 6)), V) #        Nc6

        self.assertEqual(self.g.move(W, (4, 1), (8, 5)), V) # 3. Qh5
        self.assertEqual(self.g.move(B, (7, 8), (6, 6)), V) #        Nf6

        self.assertEqual(self.g.move(W, (8, 5), (6, 7)), M) # 4. Qxf7 mat

    def test_en_passant(self):
        """'en passant' rule"""

        self.assertEqual(self.g.move(W, (1, 2), (1, 4)), V) # 1. a4
        self.assertEqual(self.g.move(B, (1, 7), (1, 6)), V) #       a6

        self.assertEqual(self.g.move(W, (1, 4), (1, 5)), V) # 2. a5
        self.assertEqual(self.g.move(B, (2, 7), (2, 5)), V) #       b5

        self.assertEqual(self.g.move(W, (1, 5), (2, 6)), V) # 3. axb6
        self.assertNotIn((2, 5), self.g.board) # The piece has been taken
        
            
if __name__ == '__main__':
    unittest.main()
    