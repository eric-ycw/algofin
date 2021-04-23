import pandas as pd
import matplotlib.pyplot as plt

from algofin.orders import OrderFlag, MarketOrder, OrderBook

class Backtest:
    def __init__(self, strategy, hist, capital, cost=0):
        self.strategy = strategy
        self.hist = hist.copy()
        self.strategy.load_hist(self.hist)
        self.initial_capital = capital
        self.cost = cost

        self.order_book = OrderBook()

    def run(self):
        for date, row in self.hist.iterrows():
            self.order_book.tick(row['Close'], date=date)
            capital = self.initial_capital + self.order_book.capital
            order = self.strategy.get_signal(date, capital)
            if order is not None and (order.adj_entry <= capital):
                self.order_book.add(order)
        self.order_book.close_all()

    def plot_pl(self):
        plt.plot([i[0] for i in self.order_book.pl_hist], label='Realized P&L')
        plt.plot([i[1] for i in self.order_book.pl_hist], label='Total P&L')
        plt.legend()
        plt.show()

    def plot_capital(self):
        plt.plot([self.initial_capital + i for i in self.order_book.capital_hist], label='Capital')
        plt.legend()
        plt.show()
