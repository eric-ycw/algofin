from enum import Enum
import pandas as pd
import matplotlib.pyplot as plt

class OrderFlag(Enum):
    BUY = 1
    HOLD = 0
    SELL = -1

class MarketOrder:
    def __init__(self, flag, price, take_profit=None, stop_loss=None, date=None, volume=1, size=None, cost=0):
        assert(flag == OrderFlag.BUY or flag == OrderFlag.SELL)

        self.flag = flag
        self.entry, self.exit = price, price
        self.adj_entry, self.adj_exit = None, None

        if size is None:
            self.volume = volume
        else:
            self.volume = size / price

        self.cost = cost
        self.adjust_prices()

        self.start_date, self.end_date = date, None
        self.take_profit, self.stop_loss = take_profit, stop_loss
        self.pl = 0
        self.hold = True

    def adjust_prices(self):
        if self.flag == OrderFlag.BUY:
            self.adj_entry = self.entry * self.volume * (1 + self.cost / 100)
            self.adj_exit = self.exit * self.volume * (1 - self.cost / 100)
        elif self.flag == OrderFlag.SELL:
            self.adj_entry = self.entry * self.volume * (1 - self.cost / 100)
            self.adj_exit = self.exit * self.volume * (1 + self.cost / 100)

    def update_pl(self):
        if self.flag == OrderFlag.BUY:
            self.pl = self.adj_exit - self.adj_entry
        elif self.flag == OrderFlag.SELL:
            self.pl = self.adj_entry - self.adj_exit

    def tick(self, price, date=None):
        self.exit = price
        self.adjust_prices()
        self.update_pl()

        if self.take_profit is not None:
            assert(self.take_profit > 1)
            if (1 + self.pl / (self.entry * self.volume)) >= self.take_profit:
                self.close(date)
        if self.stop_loss is not None:
            assert(self.stop_loss < 1)
            if (1 + self.pl / (self.entry * self.volume)) <= self.stop_loss:
                self.close(date)

    def close(self, date=None):
        self.end_date = date
        self.hold = False
        return self.pl

    def print(self):
        print(pd.Series(
            [self.flag, self.entry, self.exit, self.adj_entry, self.adj_exit, \
             self.start_date, self.end_date, self.volume, self.cost, self.pl],
            ['Order Type', 'Entry', 'Exit', 'Adjusted Entry', 'Adjusted Exit', \
             'Start Date', 'End Date', 'Volume', 'Cost %', 'Order P&L']
        ))

class OrderBook:
    def __init__(self):
        self.book = []
        self.unrealized_pl = 0
        self.pl = 0
        self.pl_hist = []
        self.capital = 0
        self.capital_hist = []

    def add(self, order):
        self.book.append(order)

    def update_pl(self):
        self.unrealized_pl = sum(order.pl for order in self.book if order.hold)
        self.pl = sum(order.pl for order in self.book if not order.hold)
        self.pl_hist.append((self.pl, self.unrealized_pl + self.pl))

    def update_capital(self):
        self.capital = 0
        for order in self.book:
            if order.hold:
                if order.flag == OrderFlag.BUY:
                    self.capital -= order.adj_entry
                elif order.flag == OrderFlag.SELL:
                    self.capital += order.adj_entry
            else:
                self.capital += order.pl
        self.capital_hist.append(self.capital)

    def tick(self, current_price, date=None):
        for order in self.book:
            if order.hold:
                order.tick(current_price, date)
        self.update_pl()
        self.update_capital()

    def close_all(self, date=None):
        for order in self.book:
            if order.hold:
                order.close(date)
        self.update_pl()
        self.update_capital()

    def close_all_buys(self, date=None):
        for order in self.book:
            if order.hold and order.flag == OrderFlag.BUY:
                order.close(date)
        self.update_pl()
        self.update_capital()

    def close_all_sells(self):
        for order in self.book:
            if order.hold and order.flag == OrderFlag.SELL:
                order.close(date)
        self.update_pl()
        self.update_capital()

    def print_orders(self):
        for order in self.book:
            order.print()
