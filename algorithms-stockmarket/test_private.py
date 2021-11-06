import numpy as np
import typing
import unittest

from stock_market import StockMarket

class TestStockMarket(unittest.TestCase):
    def test_four_stocks_two_optimal_paths(self):
        """This unittest tests the 'dynamic_programming_bottom_up()' method 
        by testing 4 stocks given in two different orders. 
        There are two different paths in which different stocks can be bought to achieve the maximum equity of 50.
        :return: Succes if both stock orders lead to the maximum equity of 50 in an optimal path, fails otherwise."""
        stock_prices_first_order = np.array([
             [10, 15, 20, 15, 10], 
             [5,  15, 10, 15, 20], 
             [30, 25, 20, 25, 30], 
             [10,  15, 30, 40, 50],], dtype=float) 

        stock_prices_second_order = np.array([
             [10,  15, 30, 40, 50], 
             [10, 15, 20, 15, 10], 
             [5,  15, 10, 15, 20], 
             [30, 25, 20, 25, 30],], dtype=float)
        
        test_case_first_order = StockMarket(5, stock_prices_first_order, 1.0)
        test_case_second_order = StockMarket(5, stock_prices_second_order, 1.0)

        test_case_first_order.dynamic_programming_bottom_up()
        test_case_second_order.dynamic_programming_bottom_up()

        last_day = len(stock_prices_second_order[0])-1 
        self.assertEqual(test_case_first_order.max_gain_on_day(last_day), test_case_second_order.max_gain_on_day(last_day))
        self.assertNotEqual(test_case_first_order.backtracing_portfolio, test_case_second_order.backtracing_portfolio)
    
    def test_low_stockprice_high_interest(self):
        """This unittest tests the dynamic_programming_bottom_up() method using an extremely high interest rate and unefficient stocks.
        The method should not buy any stocks since the interest rate is better than the profit that can be made on the stocks.
        :return: Succes if no stocks were bought, fails otherwise. """
        stock_prices = np.array([[5, 4, 4, 2],
                                [5, 3, 3, 3],
                                [5, 4, 2, 2],
                                [5, 3, 3, 1]], dtype=float)
        interest_rate = 2.0 # 200%
        test_case = StockMarket(5, stock_prices, interest_rate)
        test_case.dynamic_programming_bottom_up()
        for portfolio in set(test_case.backtracing_portfolio()):
            self.assertEqual(0, portfolio) 

    def test_interest_vs_stockprice(self): 
        """This unittest test the dynamic_programming_bottom_up() method when the interest rate gains are equal to the stock gains.
        The mthod should not buy any stocks if the interest rate gains are equal or higher than the stock gains.
        :return: Succes if no stocks were bought, fails otherwise. """
        stock_prices = np.array([[5, 10, 20, 40]], dtype=float)
        interest_rate = 2.0 # 200%
        test_case = StockMarket(5, stock_prices, interest_rate)
        test_case.dynamic_programming_bottom_up()
        for portfolio in set(test_case.backtracing_portfolio()):
            self.assertEqual(0, portfolio) 