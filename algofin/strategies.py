import numpy as np

from algofin.orders import OrderFlag, MarketOrder
from algofin.indicators import EMA

class Strategy:
    def __init__(self):
        pass

class EMACrossover(Strategy):
    def __init__(self, t1=5, t2=20, short=True, volume=1, size=None, cost=0):
        self.hist = None
        self.t1 = t1
        self.t2 = t2
        self.short = short
        self.volume = volume
        self.size = size
        self.cost = cost
        assert(self.t1 < self.t2)

    def load_hist(self, hist):
        self.hist = hist
        self.hist['EMA_'+str(self.t1)] = EMA(self.hist['Close'], t=self.t1)
        self.hist['EMA_'+str(self.t2)] = EMA(self.hist['Close'], t=self.t2)
        self.hist.dropna(inplace=True)

        self.hist['Pos'] = self.hist['EMA_'+str(self.t1)] > self.hist['EMA_'+str(self.t2)]
        self.hist['PrevPos'] = self.hist['Pos'].shift(1)

        signals = [
            (self.hist['PrevPos'] == 0) & (self.hist['Pos'] == 1),
            (self.hist['PrevPos'] == 1) & (self.hist['Pos'] == 0)
        ]

        labels = [OrderFlag.BUY, (OrderFlag.SELL if self.short else OrderFlag.HOLD)]
        self.hist['Signal'] = np.select(signals, labels, default=OrderFlag.HOLD)

        self.hist.drop(['EMA_'+str(self.t1), 'EMA_'+str(self.t2), 'Pos', 'PrevPos'], axis=1, inplace=True)


    def get_signal(self, date, capital):
        try:
            signal = self.hist.loc[date, 'Signal']
        except KeyError:
            signal = OrderFlag.HOLD

        if signal is not OrderFlag.HOLD:
            if self.size is not None:
                size = self.size * capital
            else:
                size = None
            order = MarketOrder(
                signal, self.hist.loc[date, 'Close'],
                take_profit=1.15, stop_loss=0.95,
                date=date, volume=self.volume, size=size, cost=self.cost
            )
        else:
            order = None
        return order
