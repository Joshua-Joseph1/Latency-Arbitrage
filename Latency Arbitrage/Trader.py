import pandas as pd
import numpy as np
from threading import Thread
import MetaTrader5 as mt1
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import fxcmpy
import time
import ta as ta
import requests
import datetime
pd.set_option('display.max_rows', 6000)
pd.set_option('display.max_columns', 2000)
pd.set_option('display.width', 2000)


col = ["tradeId", "amountK", "currency", "grossPL", "isBuy"]

class Trader():
    
    def __init__(self, instrument):
        self.instrument = instrument
        self.tick_data = None
        self.raw_data = None
        self.data = None 
        self.last_bar_sec = None
        self.order = None
        self.ticks = 0
        self.last_bar = None  
        
        self.avg_move = None
        self.candles = 0
        self.stop_loss = 0
        self.take_profit = 0
        self.last_traded_price = 0
        print('Connecting')
        self.api = fxcmpy.fxcmpy(access_token="56a2c43a9c41d27042ddbcae15a01f716870e248", log_level='error', log_file='fxcm_cfg.log')
        print(self.api.connection_status)
        #print(self.api.get_account_ids()[0])
        self.units = 50
        self.position = 0

    
    def get_tick_data(self, data, dataframe):
        self.ticks += 1
        recent_tick = pd.to_datetime(data["Updated"], unit = "ms")
        self.tick_data = dataframe
        #print(data)
        #print(type(data))
        #print(self.tick_data.tail(1).index[0])
        self.last_bar_sec = float((str(self.tick_data.tail(1).index[0])[14:26].replace(':','')))
        #print(self.last_bar_sec)
        #time.sleep(10)
        #print(self.tick_data.tail(1))

    def buy(self, tp, sl):
        open_trade = self.api.open_trade(account_id=1698707, symbol="NAS100", is_buy=True, amount=100, order_type='AtMarket', time_in_force='GTC', limit=tp ,stop = sl, is_in_pips=False)
        print(open_trade)
        print(tp, sl)
  
    def report_trade(self, order, going):  
        time = order.get_time()
        units = self.api.get_open_positions().amountK.iloc[-1]
        price = self.api.get_open_positions().open.iloc[-1]
        unreal_pl = self.api.get_open_positions().grossPL.sum()
        print("\n" + 100* "-")
        print("{} | {}".format(time, going))
        print("{} | units = {} | price = {} | Unreal. P&L = {}".format(time, units, price, unreal_pl))
        print(100 * "-" + "\n")


class fxProTrader():
    
    def __init__(self, instrument):
        self.instrument = instrument
        self.tick_data = pd.DataFrame()
        self.raw_data = pd.DataFrame()
        self.history = pd.DataFrame()
        self.data = None 
        self.ticks = 0
        self.last_bar = None  
        self.last_bar_sec = None
        self.api = mt1
        self.api.initialize(r"C:\Program Files\FxPro - MetaTrader 5\terminal64.exe")
        self.last_acc_balance = 0
        self.login = 5428916 
        self.password = 'mu7tW9eV'
        self.trades = 0
        self.server = 'FxPro-MT5'
        self.max_acc_bal = 0
        print(self.api.login(self.login, self.password, self.server))
        self.avg_move = None
        self.candles = 0
        self.stop_loss = 0
        self.take_profit = 0
        self.carry_over = False
        self.units = 0
        self.position = 0
        self.count_weekend_ticks = 0
    
        
    def get_tick_data(self):
        while True:
            self.count_weekend_ticks=0
            self.ticks += 1
            tick = self.api.symbol_info_tick(self.instrument)
            dict = {"time" : pd.to_datetime(tick.time, unit = 's'), "bidopen" : tick.bid, "askopen": tick.ask, "last": tick.last, "volume": tick.volume, "time_msc": pd.to_datetime(tick.time_msc, unit='ms') , "flags": tick.flags, "volume_real": tick.volume_real}
            self.tick_data = self.tick_data.append(dict, ignore_index=True)
            print(self.tick_data)

            self.last_bar_sec = float(str(pd.to_datetime(tick.time_msc, unit='ms'))[14:26].replace(':',''))

            self.candles += 1

    def buy(self, price, tp):
        deviation = 20
        print(price)
        print(tp)
        request = {
                    "action": self.api.TRADE_ACTION_DEAL,
                    "symbol": self.instrument,
                    "volume": 0.1,
                    "type": self.api.ORDER_TYPE_BUY,
                    "price": price,
                    "sl": price-1000,
                    "tp": tp,
                    "deviation": deviation,
                    "magic": 234000,
                    "comment": "python script open",
                    "type_time": self.api.ORDER_TIME_GTC,
                    "type_filling": self.api.ORDER_FILLING_IOC,
                }
        order = self.api.order_send(request)
        print(order)
        self.position=1
        


class bot(Thread):
    def __init__(self):
        self.data = pd.DataFrame()
        self.trade = False
        self.count = 0
        
    def analyse(self, broker1, broker2, count):
        while True:
            if count==0:
                print('waiting')
                time.sleep(4)
                count+=1
            if 1==1:#len(pd.DataFrame(broker1.api.get_open_positions())) < 2:
                if broker2.last_bar_sec>broker1.last_bar_sec and (list(broker2.tick_data.tail(1)['bidopen'])[0] > list(broker1.tick_data.tail(1)['Ask'])[0] ):
                #if broker2.last_bar_sec>broker1.last_bar_sec and (list(broker2.tick_data.tail(1)['askopen'])[0] < list(broker1.tick_data.tail(1)['Bid'])[0] ):
                    #print('ask = {}, bidopen = {}'.format(list(broker1.tick_data.tail(1)['Ask'])[0], list(broker2.tick_data.tail(1)['bidopen'])[0]))
                    #print(datetime.datetime.now())
                    #open_trade = broker1.api.open_trade(account_id=1698707, symbol="NAS100", is_buy=True, amount=1, order_type='AtMarket', time_in_force='GTC', limit=15000 ,stop =13000, is_in_pips=False)
                    #print(datetime.datetime.now())

                    #broker1.buy(list(broker2.tick_data.tail(1)['bidopen'])[0], list(broker1.tick_data.tail(1)['Ask'])[0] -1 )
                    dict = {"FXCM Time" : str(broker1.tick_data.tail(1).index[0]), "FXCM Bid" : float(list(broker1.tick_data.tail(1)['Bid'])[0]), "FXCM Ask": float(list(broker1.tick_data.tail(1)['Ask'])[0]),
                            "FxPro Time": str(str((str(pd.to_datetime(broker2.tick_data.tail(1)['time_msc'])).split('\n'))[0]).split('   ')[1]) , "FxPro bidopen": list(broker2.tick_data.tail(1)['bidopen'])[0], "FxPro askopen":list(broker2.tick_data.tail(1)['askopen'])[0]}
                    self.data = self.data.append(dict, ignore_index=True)
                    #self.writeData()
                    print(dict)
                    self.trade = True
                    self.count = 0    


    def keepConnectionAlive(self, broker):
        pass
    
    def writeData(self):
        print('Writing data')
        self.data.to_csv('NAS100.csv')


if __name__ == "__main__":  
    tryConnect = True

    while tryConnect:
        try:
            #fxcmTrader = Trader(instrument="NAS100")
            fxPro = fxProTrader(instrument="GOLD")
            #bot1 = bot()
            count = 0

            #Thread(target=fxcmTrader.api.subscribe_market_data("NAS100", (fxcmTrader.get_tick_data,))).start()
            Thread(target=fxPro.get_tick_data).start()
            tryConnect = False
            #Thread(target=bot1.analyse(fxcmTrader, fxPro, count)).start()
        except (requests.exceptions.ConnectionError ):
            tryConnect = True
        


