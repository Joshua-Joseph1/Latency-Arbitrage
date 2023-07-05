import datetime
import pandas as pd
import json
import requests
import socketio
import time
import sys
import engineio


socketIO = socketio.Client()


TRADING_API_URL = 'https://api-demo.fxcm.com/'
WEBSOCKET_PORT = 443
ACCESS_TOKEN = '56a2c43a9c41d27042ddbcae15a01f716870e248'

def on_connect():
    print ('Websocket connected: ' + socketIO.eio.sid)
        
def on_close():
    print ('Websocket closed.')

def on_error(str):
    print ('Websocket error.' + str)


if __name__ == '__main__':
    socketIO.connect(TRADING_API_URL +":" +str(WEBSOCKET_PORT) +"/?access_token=" +ACCESS_TOKEN)
                            

    print (socketIO.eio.sid)
    bearer_access_token="Bearer "+ socketIO.eio.sid + ACCESS_TOKEN

    params = dict(account_id=1698707, symbol="NAS100",
                      is_buy=True, amount=2, rate=0,
                      at_market=0, time_in_force="GTC",
                      order_type="AtMarket")
    '''params = {
        "account_id": "1698707",
        "symbol": "NAS100",
        "is_buy": True,
        "rate": 0,
        "amount": 3,
        "at_market": 0,
        "order_type": "AtMarket",
        "time_in_force": "GTC"
    }'''
    x=0
    while x<10:

        bef =datetime.datetime.now()
        res = requests.post(TRADING_API_URL+'trading/open_trade', params=params)
        after  =datetime.datetime.now()

        print(after - bef)
        x+=1


    print(res.status_code)

    print (bearer_access_token)
    '''socketIO.on('disconnect', on_close)
    socketIO.on('connect', on_connect)
    socketIO.on('connect_error', on_error) '''
    socketIO.disconnect()

