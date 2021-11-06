import numpy as np
import unittest

from stock_market import StockMarket


class TestStockMarket(unittest.TestCase):

    def test_portfolio_has_stock(self):
        cases = [
            [0, 0, False], [0, 1, False], [0, 2, False], [0, 3, False],
            [1, 0, True], [1, 1, False], [1, 2, False], [1, 3, False],
            [2, 0, False], [2, 1, True], [2, 2, False], [2, 3, False],
            [3, 0, True], [3, 1, True], [3, 2, False], [3, 3, False],
            [4, 0, False], [4, 1, False], [4, 2, True], [4, 3, False],
            [5, 0, True], [5, 1, False], [5, 2, True], [5, 3, False],
            [6, 0, False], [6, 1, True], [6, 2, True], [6, 3, False],
            [7, 0, True], [7, 1, True], [7, 2, True], [7, 3, False],
            [8, 0, False], [8, 1, False], [8, 2, False], [8, 3, True],
        ]
        for portfolio_idx, stock_idx, is_present in cases:
            self.assertEqual(is_present,
                             StockMarket.portfolio_has_stock(portfolio_idx,
                                                             stock_idx))

    def test_calculate_transaction(self):
        stock_prices = np.array([[1, 1], [2, 2], [4, 4]], dtype=float)
        results = [
            [0, -1, -2, -3, -4, -5, -6, -7],
            [1, 0, -1, -2, -3, -4, -5, -6],
            [2, 1, 0, -1, -2, -3, -4, -5],
            [3, 2, 1, 0, -1, -2, -3, -4],
            [4, 3, 2, 1, 0, -1, -2, -3],
            [5, 4, 3, 2, 1, 0, -1, -2],
            [6, 5, 4, 3, 2, 1, 0, -1],
            [7, 6, 5, 4, 3, 2, 1, 0],
        ]
        test_case = StockMarket(0, stock_prices, 1.0)

        for yesterday in range(len(results)):
            for today in range(len(results)):
                solution = results[yesterday][today]
                self.assertEqual(solution, test_case.calculate_transaction(1, yesterday, today))

    def test_single_stock_buy_day_zero(self):
        stock_prices = np.array([[5, 10, 5]], dtype=float)
        solutions = [5.0, 10.0, 10.0]
        test_case = StockMarket(5, stock_prices, 1.0)
        test_case.dynamic_programming_bottom_up()

        for idx, solution in enumerate(solutions):
            self.assertEqual(solution, test_case.max_gain_on_day(idx))

    def test_single_stock_buy_day_one(self):
        stock_prices = np.array([[5, 1, 10]], dtype=float)
        solutions = [5.0, 5.0, 14.0]
        test_case = StockMarket(5, stock_prices, 1.0)
        test_case.dynamic_programming_bottom_up()

        for idx, solution in enumerate(solutions):
            self.assertEqual(solution, test_case.max_gain_on_day(idx))

    def test_single_stock_buy_day_one_optimal_portfolio(self):
        stock_prices = np.array([[5, 1, 10]], dtype=float)
        solutions = [0, 1, 0]
        test_case = StockMarket(5, stock_prices, 1.0)
        test_case.dynamic_programming_bottom_up()
        self.assertEqual(solutions, test_case.backtracing_portfolio())

    def test_single_stock_do_not_buy(self):
        stock_prices = np.array([[5, 4, 3]], dtype=float)
        solutions = [5.0, 5.0, 5.0]
        test_case = StockMarket(5, stock_prices, 1.0)
        test_case.dynamic_programming_bottom_up()

        for idx, solution in enumerate(solutions):
            self.assertEqual(solution, test_case.max_gain_on_day(idx))

    def test_single_stock_do_not_buy_interest(self):
        stock_prices = np.array([[5, 9, 18]], dtype=float)
        solutions = [5.0, 10.0, 20.0]
        test_case = StockMarket(5, stock_prices, 2.0)
        test_case.dynamic_programming_bottom_up()

        for idx, solution in enumerate(solutions):
            self.assertEqual(solution, test_case.max_gain_on_day(idx))

    def test_single_stock_can_not_buy(self):
        stock_prices = np.array([[6, 12, 18]], dtype=float)
        solutions = [5.0, 5.0, 5.0]
        test_case = StockMarket(5, stock_prices, 1.0)
        test_case.dynamic_programming_bottom_up()

        for idx, solution in enumerate(solutions):
            self.assertEqual(solution, test_case.max_gain_on_day(idx))

    def test_swap_stocks(self):
        stock_prices = np.array([
            [10, 15, 20, 15, 10],
            [5,  15, 10, 15, 20],
        ], dtype=float)
        solutions = [5.0, 15.0, 20.0, 25, 30]
        test_case = StockMarket(5, stock_prices, 1.0)
        test_case.dynamic_programming_bottom_up()

        for idx, solution in enumerate(solutions):
            self.assertEqual(solution, test_case.max_gain_on_day(idx))

    def test_four_stocks(self):
        stock_prices = np.array([
            [10, 15, 20, 15, 10],
            [5,  15, 10, 15, 20],
            [30, 25, 20, 25, 30],
            [10,  15, 30, 35, 40],
        ], dtype=float)
        solutions = [5.0, 15.0, 30.0, 40.0, 50.0]
        test_case = StockMarket(5, stock_prices, 1.0)
        test_case.dynamic_programming_bottom_up()

        for idx, solution in enumerate(solutions):
            self.assertEqual(solution, test_case.max_gain_on_day(idx))
