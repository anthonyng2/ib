# -*- coding: utf-8 -*-
"""
Interaction Brokers Connection

Connection Demo
"""

from IBWrapper import IBWrapper
from ib.ext.EClientSocket import EClientSocket

accountName = "DI246990"
callback = IBWrapper()        # Instantiate IBWrapper. callback 
tws = EClientSocket(callback) # Instantiate EClientSocket and return data to callback
host = ""                     # For local host
port = 4002
clientId = 5

tws.eConnect(host, port, clientId) # Connect to TWS

tws.eDisconnect()
