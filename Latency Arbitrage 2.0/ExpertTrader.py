import pandas as pd
from threading import Thread
import MetaTrader5 as mt1
import MetaTrader5 as mt2
from time import sleep
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


if __name__ == '__main__':
    #Log in to both brokers
    mt1.initialize(r"C:\Program Files\Tickmill MT5 Terminal\terminal64.exe")
    print(mt1.login(25018545, 'E*K?pv6A9*^U', 'Tickmill-Demo'))

    mt2.initialize(r"C:\Program Files\MetaTrader 5 IC Markets (SC)\terminal64.exe")
    print(mt2.login(50887132, 'KeQVCAaX', 'ICMarketsSC-Demo'))

    #Start streaming data
    x=0
    while True:
        tm_thread = Thread(target=mt1.symbol_info_tick, args=("DE40",)).start()
        ic_thread = Thread(target=mt2.symbol_info_tick, args=("DE40",)).start()

        t_tick = tm_thread.join()
        ic_tick = ic_thread.join()
        
        print(t_tick)

        tm_last_tick  = {"time TickMill" : pd.to_datetime(t_tick.time, unit = 's'), "bidopen" : t_tick.bid, "askopen": t_tick.ask, "last": t_tick.last, "volume": t_tick.volume, "time_msc": str(pd.to_datetime(t_tick.time_msc, unit='ms')) , "flags": t_tick.flags, "volume_real": t_tick.volume_real}
        ic_last_tick  = {"time ICM" : pd.to_datetime(ic_tick.time, unit = 's'), "bidopen" : ic_tick.bid, "askopen": ic_tick.ask, "last": ic_tick.last, "volume": ic_tick.volume, "time_msc": str(pd.to_datetime(ic_tick.time_msc, unit='ms')) , "flags": ic_tick.flags, "volume_real": ic_tick.volume_real}

        if (tm_last_tick['time_msc']>ic_last_tick['time_msc']):
            print(tm_last_tick, ic_last_tick, sep='\n')

        if (tm_last_tick['time_msc']>ic_last_tick['time_msc'])and (tm_last_tick['bidopen'] > ic_last_tick['askopen']):
            print('B',tm_last_tick, ic_last_tick, sep='\n')
        if (tm_last_tick['time_msc']>ic_last_tick['time_msc'])and (tm_last_tick['askopen'] < ic_last_tick['bidopen']):
            print('S',tm_last_tick, ic_last_tick, sep='\n')
        x+=1


