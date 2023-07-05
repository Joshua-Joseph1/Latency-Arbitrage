from email import header
import json
from multiprocessing.pool import TERMINATE
import fxcm_rest_api_token as fxcm_rest_api
import time
import datetime
import pandas as pd
import MetaTrader5 as mt1
from threading import Thread



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
        self.last_price = None
        self.carry_over = False
        self.units = 0
        self.position = 0
        self.count_weekend_ticks = 0
    
        
    def get_tick_data(self):
        while True:
            self.count_weekend_ticks=0
            self.ticks += 1
            tick = self.api.symbol_info_tick(self.instrument)
            self.last_price = {"time" : pd.to_datetime(tick.time, unit = 's'), "bidopen" : tick.bid, "askopen": tick.ask, "last": tick.last, "volume": tick.volume, "time_msc": pd.to_datetime(tick.time_msc, unit='ms') , "flags": tick.flags, "volume_real": tick.volume_real}
            #self.tick_data = self.tick_data.append(dict, ignore_index=True)
            #print(pd.to_datetime(tick.time_msc, unit='ms'))

            self.last_bar_sec = '00:'+str(pd.to_datetime(tick.time_msc, unit='ms'))[14:26]#.replace(':',''))
            self.last_bar_sec = pd.to_datetime(self.last_bar_sec)
            #print(self.last_bar_sec)

            self.candles += 1


class bot():
    def __init__(self):
        self.data = pd.DataFrame()
        self.trade = False
        self.count = 0
        
    def analyse(self, broker1, broker2, count):
        while True:
            try:
                if count==0:
                    print('waiting')
                    time.sleep(4)
                    count+=1
                #print('in here')
                if 1==1:#len(pd.DataFrame(broker1.api.get_open_positions())) < 2:
                    #print(broker1.last_price['Ask'], broker2.last_price['bidopen'], broker1.last_price['Ask'] < broker2.last_price['bidopen'])
                    
                    if broker2.last_bar_sec>broker1.last_bar_sec and broker1.last_price['Ask'] < broker2.last_price['bidopen']: 
                        #print(broker1.last_price['Ask']-1,broker1.last_price['Ask'], broker2.last_price['bidopen'])
                        #bef =datetime.datetime.now()
                        trade = broker1.open_trade(account_id=1698707, symbol="NAS100", is_buy=True, amount=10,rate=0,at_market=0, time_in_force="GTC", order_type="AtMarket",
                        stop=broker1.last_price['Ask']-1, trailing_step=None, limit=broker2.last_price['bidopen'], is_in_pips=None)
                        after  =datetime.datetime.now()
                        #print(after - bef)
                        #print(trade)
                        print(broker1.last_price['Ask'], broker2.last_price['bidopen'])
                    '''elif broker2.last_bar_sec>broker1.last_bar_sec and broker1.last_price['Bid'] > broker2.last_price['askopen']: 
                        bef =datetime.datetime.now()
                        trade = broker1.open_trade(account_id=1698707, symbol="NAS100", is_buy=False, amount=30,rate=0,at_market=0, time_in_force="GTC", order_type="AtMarket",
                        stop=broker1.last_price['Bid']+1, trailing_step=None, limit=broker2.last_price['askopen'], is_in_pips=None)
                        after  =datetime.datetime.now()
                        print(after - bef)'''

            except(Exception ):
                pass


    def writeData(self):
        print('Writing data')
        self.data.to_csv('NAS100.csv')






if __name__ == '__main__':
    #fxPro = fxProTrader(instrument="#USNDAQ100")
    latencyBot = bot()
            
    fxcmTrader = fxcm_rest_api.Trader('56a2c43a9c41d27042ddbcae15a01f716870e248', 'demo')
    fxcmTrader.login()
    while len(fxcmTrader.account_list) < 1:
                time.sleep(0.1)
    account_id = fxcmTrader.account_list[0]
    count = 0

    #Thread(target=fxPro.get_tick_data).start()
    fxcmTrader.subscribe(items=str('NAS100'), handler=fxcmTrader.on_price_update)
    #Thread(target=latencyBot.analyse(fxcmTrader, fxPro, count))



