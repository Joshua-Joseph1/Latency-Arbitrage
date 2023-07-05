import pandas as pd
import json
import requests
import socketio
import time
import sys
import engineio
#print("Python version: " + sys.version)
#print("Socketio version: " + socketio.__version__)
#print("Engineio version: " + engineio.__version__)

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

    print (bearer_access_token)
    socketIO.on('disconnect', on_close)
    socketIO.on('connect', on_connect)
    socketIO.on('connect_error', on_error) 
    socketIO.disconnect()

