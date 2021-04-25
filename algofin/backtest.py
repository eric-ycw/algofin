import pandas as pd
import matplotlib.pyplot as plt
from copy import copy

from algofin.data import risk_free_rate
from algofin.orders import OrderFlag, MarketOrder, OrderBook
from algofin.utils import annual_return, sharpe

class Backtest:
    '''
    Class used to define a backtest on a single instrument.

    run(self)
        Iterate through each row of the price history Dataframe and obtain
        the trading signal from the Strategy object. The profit, return,
        and drawdown is calculated for each date and appended to the Dataframe.

    print_report(self)
        Output a backtest report with performance metrics.

    plot_pl(self)
        Plot the P&L performance throughout the backtest.

    plot_capital(self)
        Plot the available capital throughout the backtest.

    '''
    def __init__(self, strategy, hist, capital=1000000):
        self.strategy = strategy
        self.strategy.load_hist(hist)
        self.hist = self.strategy.hist.copy()

        self.start_date = self.hist.first_valid_index()
        self.end_date = self.hist.last_valid_index()

        self.initial_capital = capital
        self.ob = OrderBook()

    def run(self):
        for date, row in self.hist.iterrows():
            self.ob.tick(row['Close'], date=date)
            capital = self.initial_capital + self.ob.capital

            order = self.strategy.get_signal(date, capital)
            if order is not None and (order.adj_entry <= capital):
                self.ob.add(order)

            period = (date - self.start_date).days / 365.25
            current_value = self.ob.pl_hist[-1][1] + self.initial_capital

            self.hist.loc[date, 'Profit'] = self.ob.pl_hist[-1][1]
            self.hist.loc[date, 'Return'] = annual_return(self.initial_capital, current_value, period)

        self.hist['CumMaxProfit'] = self.hist['Profit'].cummax()
        self.hist['Drawdown'] = (self.hist['Profit'] - self.hist['CumMaxProfit']) / (self.hist['CumMaxProfit'] + self.initial_capital)

    def print_report(self):
        # Sharpe ratio
        rfr = risk_free_rate(self.start_date, self.end_date)['Close'] / 100
        diff = self.hist['Return'] - rfr
        diff.dropna(inplace=True)
        sharpe_ratio = sharpe(self.hist['Return'].iloc[-1], rfr.iloc[-1], diff.std(axis=0))

        trade_num = len(self.ob.book)

        # Win rate
        win, loss = 0, 0
        for order in self.ob.book:
            if order.pl > 0:
                win += 1
            else:
                loss += 1
        if trade_num == 0:
            win_rate = None
        else:
            win_rate = float(win) / loss

        max_drawdown = self.hist['Drawdown'].min()

        print('------------BACKTEST REPORT------------')
        print(pd.Series(
            [self.start_date, self.end_date, \
             self.initial_capital, \
             self.ob.pl_hist[-1][0], self.ob.pl_hist[-1][1], \
             self.hist['Return'].iloc[-1], sharpe_ratio, \
             trade_num, win_rate, \
             max_drawdown],
            ['Start Date', 'End Date', \
             'Initial Capital', \
             'Realized P&L', 'Total P&L', \
             'Annual Return', 'Sharpe Ratio', \
             'No. of Trades', 'Win Rate', \
             'Max Drawdown']
        ))


    def plot_pl(self):
        plt.plot([i[0] for i in self.ob.pl_hist], label='Realized P&L')
        plt.plot([i[1] for i in self.ob.pl_hist], label='Total P&L')
        plt.legend()
        plt.show()

    def plot_capital(self):
        plt.plot([self.initial_capital + i for i in self.ob.capital_hist], label='Capital')
        plt.legend()
        plt.show()

class PortfolioBacktest:
    def __init__(self, strategy, hists, capital=1000000, capital_allocation='equal', labels=None):
        self.backtests = []
        self.strategy = strategy
        self.initial_capital = capital
        self.labels = labels

        if capital_allocation == 'equal':
            self.capital_allocation = [self.initial_capital / len(hists)] * len(hists)
        elif capital_allocation == 'free':
            self.capital_allocation = [self.initial_capital] * len(hists)
        elif isinstance(capital_allocation, list):
            assert(len(capital_allocation) == len(hists))
            self.capital_allocation = [capital_allocation[i] * self.initial_capital for i in range(len(hists))]
        else:
            raise ValueError()

        for i in range(len(hists)):
            backtest = Backtest(copy(self.strategy), hists[i], capital=self.capital_allocation[i])
            self.backtests.append(backtest)

    def run(self):
        for backtest in self.backtests:
            backtest.run()
            # backtest.plot_pl()
            backtest.print_report()

        self.hist = self.backtests[0].hist['Profit'].copy()
        for backtest in self.backtests:
            self.hist += backtest.hist['Profit']

        self.hist = self.hist.to_frame()
        print(self.hist)

        # FIXME: This is atrocious
        self.pl_hists = [i.ob.pl_hist for i in self.backtests]
        self.realized_pl_hist = [0] * len(self.pl_hists[0])
        self.total_pl_hist = [0] * len(self.pl_hists[0])
        for i in range(len(self.realized_pl_hist)):
            for j in self.pl_hists:
                self.realized_pl_hist[i] += j[i][0]
                self.total_pl_hist[i] += j[i][1]

        self.capital_hist = list(map(sum, zip(*[i.ob.capital_hist for i in self.backtests])))

    def plot_pl(self):
        plt.plot(self.realized_pl_hist, label='Realized P&L')
        plt.plot(self.total_pl_hist, label='Total P&L')
        plt.legend()
        plt.show()

    def plot_capital(self):
        plt.plot([self.initial_capital + i for i in self.capital_hist], label='Capital')
        plt.legend()
        plt.show()

    def plot_pl_breakdown(self):
        for i in range(len(self.backtests)):
            if self.labels is not None:
                label_str = self.labels[i]
            else:
                label_str = str(i)
            plt.plot([j[1] for j in self.backtests[i].ob.pl_hist], label=label_str + ' P&L')

        plt.legend()
        plt.show()
