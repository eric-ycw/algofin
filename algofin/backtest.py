import pandas as pd
import matplotlib.pyplot as plt

from algofin.data import risk_free_rate
from algofin.orders import OrderFlag, MarketOrder, OrderBook
from algofin.utils import annual_return, sharpe

class Backtest:
    def __init__(self, strategy, hist, capital=1000000):
        self.strategy = strategy
        self.strategy.load_hist(hist)

        self.hist = self.strategy.hist.copy()
        self.start_date = self.hist.first_valid_index()
        self.end_date = self.hist.last_valid_index()

        self.initial_capital = capital
        self.cost = self.strategy.cost

        self.order_book = OrderBook()

    def run(self):
        for date, row in self.hist.iterrows():
            self.order_book.tick(row['Close'], date=date)
            capital = self.initial_capital + self.order_book.capital
            order = self.strategy.get_signal(date, capital)
            if order is not None and (order.adj_entry <= capital):
                self.order_book.add(order)


            period = (date - self.start_date).days / 365.25
            current_value = self.order_book.pl_hist[-1][1] + self.initial_capital

            self.hist.loc[date, 'Profit'] = self.order_book.pl_hist[-1][1]
            self.hist.loc[date, 'Return'] = annual_return(self.initial_capital, current_value, period)

        self.hist['CumMaxProfit'] = self.hist['Profit'].cummax()
        self.hist['Drawdown'] = (self.hist['Profit'] - self.hist['CumMaxProfit']) / (self.hist['CumMaxProfit'] + self.initial_capital)

    def print_report(self):
        print(self.hist)
        # Sharpe ratio
        rfr = risk_free_rate(self.start_date, self.end_date)['Close'] / 100
        diff = self.hist['Return'] - rfr
        diff.dropna(inplace=True)
        sharpe_ratio = sharpe(self.hist['Return'].iloc[-1], rfr.iloc[-1], diff.std(axis=0))

        trade_num = len(self.order_book.book)

        # Win rate
        win, loss = 0, 0
        for order in self.order_book.book:
            if order.pl > 0:
                win += 1
            else:
                loss += 1
        if trade_num == 0:
            win_rate = None
        else:
            win_rate = float(win) / loss

        max_drawdown = self.hist['Drawdown'].min()

        print('----------BACKTEST REPORT----------')
        print(pd.Series(
            [self.start_date, self.end_date, \
             self.order_book.pl_hist[-1][0], self.order_book.pl_hist[-1][1], \
             self.hist['Return'].iloc[-1], sharpe_ratio, \
             trade_num, win_rate, \
             max_drawdown],
            ['Start Date', 'End Date', \
             'Realized P&L', 'Total P&L', \
             'Annual Return', 'Sharpe Ratio', \
             'No. of Trades', 'Win Rate', \
             'Max Drawdown']
        ))




    def plot_pl(self):
        plt.plot([i[0] for i in self.order_book.pl_hist], label='Realized P&L')
        plt.plot([i[1] for i in self.order_book.pl_hist], label='Total P&L')
        plt.legend()
        plt.show()

    def plot_capital(self):
        plt.plot([self.initial_capital + i for i in self.order_book.capital_hist], label='Capital')
        plt.legend()
        plt.show()
