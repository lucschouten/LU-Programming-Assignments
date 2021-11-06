import numpy as np
import typing


class StockMarket(object):

    def __init__(self, b0, stock_prices: np.array, interest_factor: float):
        """
        Initializes the relevant parameters

        :param b0: The budget available on day 0
        :param stock_prices: 2D numpy array, where stock_prices[i, j] is the
        price of stock j on day i
        :param interest_factor: The interest factor that is allocated to money
        that is on the bank (not invested in stocks)
        """
        self.b0 = b0
        self.stock_prices = stock_prices
        self.interest_factor = interest_factor
        self.n_portfolios = 2 ** self.stock_prices.shape[0]
        self.n_days = self.stock_prices.shape[1]
        self.memory = np.zeros(
            shape=(self.n_portfolios, self.n_days), dtype=float)
    @staticmethod
    def portfolio_has_stock(portfolio_idx: int, stock_idx: int) -> bool:
        """
        Determine for a given portfolio, whether a given stock was in it

        :param portfolio_idx: the index of the portfolio, expressed as integer
        :param stock_idx: the index of the stock
        :return: true or false, whether the stock was present in the portfolio
        """
        btsr = "{0:b}".format(portfolio_idx)
        if len(btsr) >= stock_idx + 1:
            if btsr[(-1*stock_idx)-1] == '1':
                return True
        return False

    def calculate_transaction(self, day_idx: int, portfolio_idx_yesterday: int,
                              portfolio_idx_today: int) -> float:
        """
        Given a two stock portfolios (the one of today and the one of
        yesterday), determine the cost of the transaction. Note that each stock
        that was in yesterdays portfolio is sold and will count positive to the
        transaction, whereas each stock that was not in yesterdays portfolio and
        is in today's portfolio was bought, and will count negatively to the
        transaction.

        :param day_idx: the index of today's day (note that yesterday was
        day_idx - 1)
        :param portfolio_idx_yesterday: the index of today's (yesterdays) portfolio,
        expressed as integer
        :param portfolio_idx_today: the index of yesterday's (yesterdays) portfolio,
        expressed as integer

        :return: the transaction cost from yesterday's portfolio to today's
        portfolio
        """
        length_longest_portfolio = len("{0:b}".format(max(portfolio_idx_yesterday, portfolio_idx_today)))
        #We make the representation of both portfolios the same length for easy comparison
        portfolio_today = "{0:b}".format(portfolio_idx_today).rjust(length_longest_portfolio, '0')
        portfolio_yesterday = "{0:b}".format(portfolio_idx_yesterday).rjust(length_longest_portfolio, '0') 
        transaction_cost = float()
        difference_length_stocks_portfolio = abs(len(self.stock_prices)-len(portfolio_today)) 
        for i in range(length_longest_portfolio):
            if portfolio_today[i] != portfolio_yesterday[i]:
                if portfolio_today[i] == '1': #When we buy the stock
                    transaction_cost -= self.stock_prices[(-1*i)-1-difference_length_stocks_portfolio][day_idx]  
                elif portfolio_today[i] == '0':#When we sell the stock
                    transaction_cost += self.stock_prices[(-1*i)-1-difference_length_stocks_portfolio][day_idx] 
        return transaction_cost

    def dynamic_programming_bottom_up(self) -> None:
        """
        Fills the complete memory table in a bottom up fashion.
        """
        for day in range(self.n_days):
            max_liquidized_equity = -1 
            for possible_portfolio_yesterday_idx in range(self.n_portfolios):
                if self.memory[possible_portfolio_yesterday_idx][day-1] == -1: 
                    continue #In this case is not possible to go from yesterdays portfolio to the portfolio looked at
                else:  
                    #Yesterdays budget with interest + the worth of yesterdays portfolio today 
                    liquidized_equity = self.memory[possible_portfolio_yesterday_idx][day-1]*self.interest_factor + self.calculate_transaction(day,possible_portfolio_yesterday_idx,0) 
                    if liquidized_equity > max_liquidized_equity: 
                        #Store the maximum amount of budget which can be retrieved from yesterday to spend today
                        max_liquidized_equity = liquidized_equity 

            for possible_portfolio_idx in range(self.n_portfolios):
                if day == 0:
                    remaining_budget = self.b0 + self.calculate_transaction(day,0,possible_portfolio_idx)
                    if remaining_budget >= 0: #We can buy this portfolio
                        self.memory[possible_portfolio_idx][day] = remaining_budget
                    else:
                        self.memory[possible_portfolio_idx][day] = -1 #The portfolio is not reachable with start budget
                else: 
                    max_remaining_budget = -1 
                    cost_portfolio = self.calculate_transaction(day,0,possible_portfolio_idx)
                    if max_liquidized_equity >= abs(cost_portfolio): #Can we buy the portfolio with the liquidized equity 
                        max_remaining_budget = max_liquidized_equity + cost_portfolio
                    self.memory[possible_portfolio_idx][day] = max_remaining_budget 

    def max_gain_on_day(self, day: int) -> float:
        """
        Returns for a given day the maximum budget that can be obtained
        :param day: The day we are interested in
        :return: The maximum budget that can be obtained  
        """
        return self.memory[0][day] #Max budget of the day is always on the top of the column 
    
    def backtracing_portfolio(self) -> typing.List[int]:
        """Returns a sequence of portfolios how to come to the optimal solution

        Optional - you can still pass the assignment if you do not hand this in,
        however it will count towards your grade.

        :return: A list ,where each index corresponds to a day and with the portfolio index as elements, containing the optimal solution.
        """
        solution = list()
        best_solution_idx = 0
        solution.append(0)
        for day in range(self.n_days-1, 0, -1):
            #The best budget of today that can be achieved. 
            best_solution_equity = self.memory[0][day] 
            if day >= 1:
                for portfolioidx in range(self.n_portfolios):
                    budget = self.memory[portfolioidx][day-1]
                    if budget != -1:
                        portfolio_yesterday_worth_today = budget*self.interest_factor + self.calculate_transaction(day, portfolioidx, 0)
                        if portfolio_yesterday_worth_today == best_solution_equity: #Yesterdays portfolio that yields the sought budget for today 
                            solution.insert(0, portfolioidx)
                            best_solution_idx = portfolioidx
                            break #Break because multiple paths to the max budget of today from yesterday may exist 
        return solution

