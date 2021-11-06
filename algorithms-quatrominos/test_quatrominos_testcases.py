import numpy as np
import unittest

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
    tile1112 = (1, 1, 1, 2)
    tile2211 = (2, 2, 1, 1)
    tile2411 = (2, 4, 1, 1)
    tile5315 = (5, 3, 1, 5)
    tile1414 = (1, 4, 1, 4)
    tile1114 = (1, 1, 1, 4)


class GameStateFactory(object):

    @staticmethod
    def get_big_board_unable_to_place() -> Quatrominos:
        player0 = {
            TileFactory.tile1111, TileFactory.tile1112,
            TileFactory.tile1212, TileFactory.tile2211,
        }
        player1 = {
            TileFactory.tile1111, TileFactory.tile2222,
            TileFactory.tile1113, TileFactory.tile3333,
        }
        board = np.full((5, 5, 4), -1)
        game_state = Quatrominos(player0, player1, board, 0)
        return game_state

    @staticmethod
    def get_small_board_too_many_tiles() -> Quatrominos:
        player0 = {
            TileFactory.tile2222,TileFactory.tile2222,
            TileFactory.tile2222,TileFactory.tile2222,
            TileFactory.tile2222,TileFactory.tile2222,
        }
        player1 = {
            TileFactory.tile2222,TileFactory.tile2222,
            TileFactory.tile2222,TileFactory.tile2222,
            TileFactory.tile2222,TileFactory.tile2222,
        }
        board = np.full((3, 3, 4), -1)
        game_state = Quatrominos(player0, player1, board, 0)
        return game_state

    @staticmethod
    def get_small_board_greedy_not_optimal() -> Quatrominos:
        player0 = {
            TileFactory.tile1114,
            TileFactory.tile2222,
            }
        player1 = {
            TileFactory.tile5315,
            TileFactory.tile1414,
            }
        board = np.full((3, 3, 4), -1)
        game_state = Quatrominos(player0, player1, board, 0)
        return game_state


class TestQuatrominos(unittest.TestCase):

    def test_current_player_can_win_cannot_place(self):
        game_state = GameStateFactory.get_big_board_unable_to_place()
        game_state.board[2, 2] = (4, 4, 4, 4)
        result = game_state.current_player_can_win()
        self.assertFalse(result)


    def test_current_player_can_win_too_many_tiles(self):
        game_state = GameStateFactory.get_small_board_too_many_tiles()
        game_state.board[1, 1] = (2, 2, 2, 2)
        result = game_state.current_player_can_win()
        self.assertTrue(result)


    def test_current_player_can_win_optimal_adverserial(self):
        game_state = GameStateFactory.get_small_board_greedy_not_optimal()
        game_state.board[1,0] = (4, 1, 2, 1)
        game_state.board[1, 1] = (2, 3, 0, 1)
        game_state.board[1, 2] = (3, 3, 3, 3)
        game_state.print_current_state()
        result = game_state.current_player_can_win()
        self.assertTrue(result)#Player 0 wins when he does an optimal move.

    def test_current_player_can_win_greedy_adverserial(self):
        game_state = GameStateFactory.get_small_board_greedy_not_optimal()
        game_state.board[1, 0] = (4, 1, 2, 1)
        game_state.board[1, 1] = (2, 3, 0, 1)
        game_state.board[1, 2] = (3, 3, 3, 3)
        greedy_move = game_state.best_move_greedy()
        game_state.board[greedy_move[0],greedy_move[1]] = greedy_move[2]
        game_state.player_hand[0].remove(TileFactory.tile2222)
        game_state.player_on_turn = 1 #Because player 0 did his first move, player 1 is on turn
        result = game_state.current_player_can_win() # If player 1 can win then we lose
        self.assertTrue(result)#Player 1 wins as player 0 play greedy.
