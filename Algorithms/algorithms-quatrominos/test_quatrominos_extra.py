import numpy as np
import unittest
import timeit
from quatrominos import Quatrominos


class TileFactory(object):
    tile1111 = (1, 1, 1, 1)
    tile1212 = (1, 2, 1, 2)
    tile1113 = (1, 1, 1, 3)
    tile1313 = (1, 3, 1, 3)
    tile1414 = (1, 4, 1, 4)
    tile2222 = (2, 2, 2, 2)
    tile3333 = (3, 3, 3, 3)
    tile2411 = (2, 4, 1, 1)


class GameStateFactory(object):

    @staticmethod
    def get_big_board() -> Quatrominos:
        player0 = {
            TileFactory.tile1111, TileFactory.tile1113,
            TileFactory.tile1212, TileFactory.tile1313,
            TileFactory.tile1414
        }
        player1 = {
            TileFactory.tile1414, TileFactory.tile2222,
            TileFactory.tile3333, TileFactory.tile2411,
            TileFactory.tile1111
        }
        board = np.full((5, 5, 4), -1)
        game_state = Quatrominos(player0, player1, board, 0)
        return game_state


class TestQuatrominos(unittest.TestCase):

    def test_current_player_can_win_big(self):
        start = timeit.default_timer()

        game_state = GameStateFactory.get_big_board()
        result = game_state.current_player_can_win()
        stop = timeit.default_timer()

        print('Time: ', stop - start)  
        self.assertTrue(result)

    def test_current_player_can_win_big_after_2moves(self):
        game_state = GameStateFactory.get_big_board()
        # winning move for player 0:
        game_state.board[2, 2] = (1, 2, 2, 1)
        game_state.player_hand[0].remove(TileFactory.tile1212)
        # any move for player 1, since none are winning
        game_state.board[1, 2] = TileFactory.tile2411
        game_state.player_hand[1].remove(TileFactory.tile2411)

        result = game_state.current_player_can_win()
        self.assertTrue(result)

    def test_current_player_can_win_big_after_4moves(self):
        game_state = GameStateFactory.get_big_board()
        # winning move for player 0:
        game_state.board[2, 2] = (1, 2, 2, 1)
        game_state.player_hand[0].remove(TileFactory.tile1212)
        # any move for player 1, since none are winning
        game_state.board[1, 2] = TileFactory.tile2411
        game_state.player_hand[1].remove(TileFactory.tile2411)
        # winning move for player 0:
        game_state.board[2, 1] = (3, 1, 3, 1)
        game_state.player_hand[0].remove(TileFactory.tile1313)
        # any move for player 1, since none are winning
        game_state.board[0, 2] = (2, 2, 2, 2)
        game_state.player_hand[1].remove(TileFactory.tile2222)

        result = game_state.current_player_can_win()
        self.assertTrue(result)

    def test_current_player_can_win_big_after_6moves(self):
        game_state = GameStateFactory.get_big_board()
        # winning move for player 0:
        game_state.board[2, 2] = (1, 2, 2, 1)
        game_state.player_hand[0].remove(TileFactory.tile1212)
        # any move for player 1, since none are winning
        game_state.board[1, 2] = TileFactory.tile2411
        game_state.player_hand[1].remove(TileFactory.tile2411)

        # winning move for player 0:
        game_state.board[2, 1] = (3, 1, 3, 1)
        game_state.player_hand[0].remove(TileFactory.tile1313)
        # any move for player 1, since none are winning
        game_state.board[0, 2] = (2, 2, 2, 2)
        game_state.player_hand[1].remove(TileFactory.tile2222)

        # winning move for player 0:
        game_state.board[3, 1] = (1, 1, 1, 3)
        game_state.player_hand[0].remove(TileFactory.tile1113)
        # any move for player 1, since none are winning
        game_state.board[4, 1] = TileFactory.tile1414
        game_state.player_hand[1].remove(TileFactory.tile1414)

        result = game_state.current_player_can_win()
        self.assertTrue(result)
