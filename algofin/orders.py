from enum import Enum

class OrderFlag(Enum):
    BUY = 1
    HOLD = 0
    SELL = -1

class MarketOrder:
    def __init__(self, id, flag, start_price, volume=1, cost=0):
        assert(flag == OrderFlag.BUY or flag == OrderFlag.SELL)

        self.id = id
        self.flag = flag
        self.start_price = start_price
        self.end_price = start_price
        self.volume = volume
        self.cost = cost
        self.unrealized_pl = 0
        self.pl = 0
        self.hold = True

    def tick(self, current_price):
        self.end_price = current_price
        if self.flag == OrderFlag.BUY:
            self.unrealized_pl = (
                self.end_price * self.volume * (1 - self.cost / 100) - \
                self.start_price *  self.volume * (1 + self.cost / 100)
            )
        elif self.flag == OrderFlag.SELL:
            self.unrealized_pl = (
                self.start_price * self.volume * (1 - self.cost / 100) - \
                self.end_price * self.volume * (1 + self.cost / 100)
            )

    def close(self):
        self.pl = self.unrealized_pl
        self.unrealized_pl = 0
        self.hold = False

class OrderBook:
    def __init__(self):
        self.book = []
        self.unrealized_pl = 0
        self.pl = 0

    def add(self, ord):
        self.book.append(ord)

    def tick(self, current_price):
        a, b = 0, 0

        for ord in self.book:
            if ord.hold:
                ord.tick(current_price)
                a += ord.unrealized_pl
            else:
                b += ord.pl

        self.unrealized_pl, self.pl = a, b

    def close_all(self):
        for ord in self.book:
            if ord.hold:
                self.pl += ord.unrealized_pl
                ord.unrealized_pl = 0
                ord.hold = False
        self.unrealized_pl = 0

    def report(self):
        print('Unrealized P/L:', self.unrealized_pl)
        print('Realized P/L:', self.pl)
        print('\n')
