'''
This is a very rough implementation of long short SMA 
Do not trade with this.
It is for education purpose. Use at your own risk.

obtain_hist_data :- extract historical data. 
SMA :- calculate moving averages

check_existin_pos :- check if we already have a position.

'''


import pandas as pd
import numpy as np
import time
from datetime import datetime
from IBWrapper import IBWrapper, contract
from ib.ext.EClientSocket import EClientSocket

def obtain_hist_data(tws, callback):
	# Request historical data for calculation of moving averages
	# the historical lookback is hardcoded
	# as is the frequency
	# should really check the data returned is the same ID we called.
	# fixed to look back from today

	tickerId = 9004
	data_endtime = datetime.now().strftime("%Y%m%d %H:%M:%S")
	tws.reqHistoricalData(tickerId, 
	                      contract_Details, 
	                      data_endtime,
	                      "6 M", 
	                      "1 day", 
	                      "TRADES", 
	                      0, 
	                      1)
	time.sleep(2)
	data = pd.DataFrame(callback.historical_Data, 
	                    columns = ["reqId", "date", "open",
	                               "high", "low", "close", 
	                               "volume", "count", "WAP", 
	                               "hasGaps"])
	return data


def SMA(data, short_length, long_length):
	# calculate two moving averages
	data = data.dropna()
	short_SMA = data['close'].rolling(short_length).mean()
	long_SMA = data['close'].rolling(long_length).mean()

	return short_SMA.iloc[-1], long_SMA.iloc[-1]

def check_existing_pos():
	# 0 is no position, 1 means we have existing position
	# we need to write an algo to send request to IB to check
	# whether we have existing position
	# you will need a proper identifier for your position.
	pos = 1 
	return pos

# connect
accountName = "DU000000"
callback = IBWrapper()             # Instantiate IBWrapper. callback 
tws = EClientSocket(callback)      # Instantiate EClientSocket and return data to callback
host = ""
port = 4002
clientId = 4002
order_id = 1001

tws.eConnect(host, port, clientId) # Connect to TWS

# Let's work with APPLE stock.
create = contract()
callback.initiate_variables()
contract_Details = create.create_contract('AAPL', 'STK', 'SMART', 'USD')

'''
This should be the beginning of the while loop
This is an infinite loop.
'''
while 1:
	# let's get some historical data    
	data = obtain_hist_data(tws, callback)


	short_SMA, long_SMA = SMA(data, 5, 10)
	print("short_SMA {}, long_SMA {}".format(short_SMA, long_SMA))

	# trading decision
	# ideally we need a check to see if we already have a position. 
	# Else we keep sending a buy 
	if short_SMA > long_SMA:
		pos = check_existing_pos()
		print(pos)
		if not pos:
			print("[INFO] order placing...")
			tws.reqIds(1)
			order_id = callback.next_ValidId + 1
			# placing order
			order_info = create.create_order(accountName, "MKT", 250, "BUY")
			tws.placeOrder(order_id, contract_Details, order_info)
			time.sleep(2)
			order_status_update = pd.DataFrame(callback.order_Status,
				columns = ['orderId', 'status', 'filled', 'remaining', 'avgFillPrice',
				'permId', 'parentId', 'lastFillPrice', 'clientId', 'whyHeld'])
			# if the order is filled, it should be picked up by the 
			# check_existing_pos function. The place order should not
			# be fired.

# disconnnet
tws.eDisconnect()

