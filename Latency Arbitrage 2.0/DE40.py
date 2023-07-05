import pandas as pd
from threading import Thread
import MetaTrader5 as mt1
import MetaTrader5 as mt2
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

class TickMillTrader():
    
    def __init__(self, instrument):
        self.instrument = instrument
        self.last_tick = {}
        self.api = mt1
        self.api.initialize(r"C:\Program Files\Tickmill MT5 Terminal\terminal64.exe")
        self.login = 25018545 
        self.password = 'E*K?pv6A9*^U'
        self.server = 'Tickmill-Demo'
        self.max_acc_bal = 0
        print(self.api.login(self.login, self.password, self.server))
        
    def get_tick_data(self):
        while True:
            tick = self.api.symbol_info_tick(self.instrument)
            self.last_tick = {"time TickMill" : pd.to_datetime(tick.time, unit = 's'), "bidopen" : tick.bid, "askopen": tick.ask, "last": tick.last, "volume": tick.volume, "time_msc": str(pd.to_datetime(tick.time_msc, unit='ms')) , "flags": tick.flags, "volume_real": tick.volume_real}

        
class ICMTrader():
    def __init__(self, instrument):
        self.instrument = instrument
        self.last_tick = {}
        self.api = mt2
        self.api.initialize(r"C:\Program Files\MetaTrader 5 IC Markets (SC)\terminal64.exe")
        self.login = 50891300 
        self.password = 'J7y7iwL5'
        self.server = 'ICMarketsSC-Demo'
        print(self.api.login(self.login, self.password, self.server))
        
    def get_tick_data(self):
        while True:
            tick = self.api.symbol_info_tick(self.instrument)
            self.last_tick  = {"time ICM" : pd.to_datetime(tick.time, unit = 's'), "bidopen" : tick.bid, "askopen": tick.ask, "last": tick.last, "volume": tick.volume, "time_msc": str(pd.to_datetime(tick.time_msc, unit='ms')) , "flags": tick.flags, "volume_real": tick.volume_real}


class ArbitrageBot():
    def analyse_time(self, tickmill, icmarkets):
        while True:
            if (tickmill.last_tick['time_msc']<icmarkets.last_tick['time_msc']):
                print(tickmill.last_tick, icmarkets.last_tick, sep='\n')
                
    def analyse_buy(self, tickmill, icmarkets):
        x = 0
        while True:
            if (tickmill.last_tick['time_msc']>icmarkets.last_tick['time_msc'])and (tickmill.last_tick['bidopen'] > icmarkets.last_tick['askopen']):
                x += (tickmill.last_tick['bidopen']-icmarkets.last_tick['askopen'])
                request = {
                    "action": icmarkets.api.TRADE_ACTION_DEAL,
                    "symbol": "DE40",
                    "volume": 0.1,
                    "type": icmarkets.api.ORDER_TYPE_BUY,
                    "price": icmarkets.last_tick['askopen'],
                    "sl": icmarkets.last_tick['askopen']-1,
                    "tp": tickmill.last_tick['bidopen'],
                    "deviation": 0,
                    "magic": 234000,
                    "comment": "python script open",
                    "type_time": icmarkets.api.ORDER_TIME_GTC,
                    "type_filling": icmarkets.api.ORDER_FILLING_IOC,
                }
                icmarkets.api.order_send(request)
                print('Bought')

    def analyse_sell(self, tickmill, icmarkets):
        y = 0
        while True:
            if (tickmill.last_tick['time_msc']>icmarkets.last_tick['time_msc'])and (tickmill.last_tick['askopen'] < icmarkets.last_tick['bidopen']):
                y += (icmarkets.last_tick['bidopen']-tickmill.last_tick['askopen'])
                
                request = {
                    "action": icmarkets.api.TRADE_ACTION_DEAL,
                    "symbol": "DE40",
                    "volume": 0.1,
                    "type": icmarkets.api.ORDER_TYPE_SELL,
                    "price": icmarkets.last_tick['bidopen'],
                    "sl": icmarkets.last_tick['bidopen']+1,
                    "tp": tickmill.last_tick['askopen'],
                    "deviation": 0,
                    "magic": 234000,
                    "comment": "python script open",
                    "type_time": icmarkets.api.ORDER_TIME_GTC,
                    "type_filling": icmarkets.api.ORDER_FILLING_IOC,
                }
                icmarkets.api.order_send(request)
                print('Sold')
        


if __name__ == '__main__':
    trader = ArbitrageBot()
    tickmill = TickMillTrader(instrument="DE40")
    icmarkets = ICMTrader(instrument="DE40")

    Thread(target=tickmill.get_tick_data).start()
    Thread(target=icmarkets.get_tick_data).start()
    Thread(target=trader.analyse_time,args=(tickmill,icmarkets,)).start()
    #Thread(target=trader.analyse_buy,args=(tickmill,icmarkets,)).start()
    #Thread(target=trader.analyse_sell,args=(tickmill,icmarkets,)).start()
    
        
    
    