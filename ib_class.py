import time
from datetime import datetime
from IBWrapper import IBWrapper, contract
from ib.ext.EClientSocket import EClientSocket
from ib.ext.ScannerSubscription import ScannerSubscription
from __future__ import print_function

if __name__=="__main__":
    callback = IBWrapper()          # Instantiate IBWrapper 
    tws = EClientSocket(callback)   # Instantiate EClientSocket
    host = ""
    port = 7496
    clientId = 5000
    tws.eConnect(host, port, clientId)     # Connect to TWS
    tws.setServerLogLevel(5)
    accountName = "DU123456"        # Change to your own account
    create = contract()             # Instantiate contract class
    
    # Initiate attributes to receive data. At some point we need a separate class for this
    callback.initiate_variables()
    
    # Account and Portfolio ##############################################################
    # reqAccountUpdates   --->   updateAccountTime      self.update_AccountTime
    #                            updateAccountValue     self.update_AccountValue
    #                            updatePortfolio        self.update_Portfolio
    # accountDownloadEnd                                self.accountDownloadEnd_flag
    # reqAccountSummary   --->   accountSummary         self.account_Summary
    # cancelAccountSummary
    # accountSummaryEnd                                 self.account_SummaryEnd_flag
    # reqPositions        --->   position               self.update_Position
    # cancelPositions
    # positionEnd                                       self.positionEnd_flag
    ###################################################################################'''
    print "Testing Account and Portfolio \n"
    tws.reqAccountUpdates(1, accountName)
    tws.reqAccountSummary(1,"All","NetLiquidation")
    #tws.cancelAccountSummary(1)
    tws.reqPositions()
    #tws.cancelPositions()
    





    # Orders #############################################################################
    # placeOrder           --->   orderStatus**         self.order_Status
    # cancelorder                                
    #                      --->   openOrderEnd          self.open_OrderEnd_flag            
    # reqOpenOrders        --->   openOrder*            self.open_Order
    #                      --->   orderStatus** 
    # reqAllOpenOrders     --->   openOrder*
    #                      --->   orderStatus**
    # reqAutoOpenOrders    --->   openOrder*
    #                      --->   orderStatus**
    # reqIds               --->   nextValidId           self.next_ValidId
    #                      --->   deltaNeutralValidation
    # exerciseOptions   
    # reqGlobalCancel
    ###################################################################################'''
    print "Testing Orders Group \n"
    # Example 1 - placing order to buy stock
    tws.reqIds(1)   # Need to request next valid order Id
    time.sleep(2)   # wait for response from server
    order_id = callback.next_ValidId
    contract_info1 = create.create_contract('GOOG', 'STK', 'SMART', 'USD')
    order_info1 = create.create_order(accountName, 'MKT', 100, 'BUY')
    tws.placeOrder(order_id, contract_info1, order_info1)
    
    # Example 2 - placing order to buy FX
    tws.reqIds(1)
    time.sleep(1)
    order_id = callback.next_ValidId
    contract_info2 = create.create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')
    order_info2 = create.create_order(accountName, 'MKT', 100000, 'BUY')
    tws.placeOrder(order_id, contract_info2, order_info2)    

    #tws.cancelOrder(order_id)   # Cancel example 2 order
    #tws.reqOpenOrders()         
    #tws.reqAllOpenOrders()
    #tws.reqAutoOpenOrders(1)    # clientId had to be 0 for this to work
    tws.reqGlobalCancel()
    
    
    
    

    # Market Data ########################################################################
    # reqMktData           --->   tickPrice             self.tick_Price
    #                      --->   tickSize              self.tick_Size
    #                      --->   tickOptionComputation self.tick_OptionComputation
    #                      --->   tickGeneric           self.tick_Generic
    #                      --->   tickString            self.tick_String
    #                      --->   tickEFP               self.tick_EFP
    #                      --->   tickSnapshotEnd       self.tickSnapshotEnd_flag
    # cancelMktData                                
    # calculateImpliedVolatility >tickOptionComputation self.tick_OptionComputation
    # cancelcalculateImpliedVolatility
    # calculateOptionPrice --->   tickOptionComputation self.tick_OptionComputation
    # cancelCalculateOptionPrice
    # reqMktDataType       --->   marketDataType        self.market_DataType
    ###################################################################################'''    
    '''print "Testing Market Data Group \n"
    contract_info3 = create.create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')
    tws.reqMktData(1, contract_info3, "", False)
    
    contract_info4 = create.create_contract('NFLX 160318C00100000', 
                                            'OPT', 'SMART', 'USD', 
                                            'CALL', '100', '20160318', 
                                            100, "NFLX")
    tws.calculateImpliedVolatility(2, contract_info4, 3.60, 94.41)
    tws.calculateOptionPrice(3, contract_info4, 0.42, 94.41)
    tws.reqMarketDataType(2)                            # need to test this when mkt opens
    time.sleep(2)
    tws.cancelMktData(1)
    tws.cancelCalculateImpliedVolatility(2)
    tws.cancelCalculateOptionPrice(3)

    
    
    
    
    # Connection and Server ##############################################################
    # EClientSocket
    # eConnect                     
    # eDisconnect          --->   connectionClosed      
    # isConnected
    # setServerLogLevel
    # reqCurrentTime       --->   currentTime           self.current_Time
    # serverVersion
    # TwsConnectionTime
    #                      --->   error
    ###################################################################################'''       
    print "Testing Connection and Server Group \n"
    print  tws.isConnected()
    tws.setServerLogLevel(5)
    tws.reqCurrentTime()
    print "Server Version " + str(tws.serverVersion())
    print "TWS Connection Time %s " % tws.TwsConnectionTime()





    # Executions #########################################################################
    # reqExecutions        --->   execDetails           self.exec_Details_reqId
    #                                                   self.exec_Details_contract
    #                                                   self.exec_Details_execution
    #                      --->   execDetailsEnd        self.exec_DetailsEnd_flag
    #                      --->   commissionReport      self.commission_Report
    ###################################################################################''' 
    print "Testing Executions Group \n"
    order_id = []
    tws.reqIds(1)
    while not order_id:
        time.sleep(0.1)
        order_id = callback.next_ValidId
        print "waiting for id"
    order_id = callback.next_ValidId
    print ("Just got it. The next order id is: ", order_id)
    contract_info5 = create.create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')
    order_info5 = create.create_order(accountName, 'MKT', 100000, 'BUY')
    tws.placeOrder(order_id, contract_info5, order_info5)    
    time.sleep(2)
    tws.reqExecutions(0, create.exec_filter(9999, accountName, contract_info5))


    
    

    # Contract ###########################################################################
    # reqContractDetails   --->   contractDetails       self.contract_Details_reqId
    #                                                   self.contract_Details
    #                      --->   contractDetailsEnd    self.contract_DetailsEnd_reqId
    #                                                   self.contract_Details_flag
    #                      --->   bondContractDetails   self.bond_ContractDetails_reqId
    #                                                   self.bond_ContractDetails
    ###################################################################################'''  
    print "Testing Contract Group \n"
    # Example 1 - Option
    contract_Details6 = create.create_contract('NFLX 160318C00100000', 'OPT', 'SMART', 
                                               'USD', 'CALL', '100', '20160318', 
                                               100, "NFLX")
    tws.reqContractDetails(5000, contract_Details6)
    while not callback.contract_Details_flag:
        time.sleep(1)
    callback.contract_Details_flag = False
    print callback.contract_Details_reqId    
    print callback.contract_Details.__dict__   

    # Example 2 - Stock                                               
    contract_Details7 = create.create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')
    tws.reqContractDetails(5001, contract_Details7)
    while not callback.contract_Details_flag:
        time.sleep(1)
    callback.contract_Details_flag = False
    print callback.contract_Details_reqId    
    print callback.contract_Details.__dict__    
    
    # Example 3 - FX    
    contract_Details8 = create.create_contract('IBCID143913442', 
                                                'BOND', 'SMART', 
                                                'USD','CORP')      
    tws.reqContractDetails(5002, contract_Details8)
    while not callback.contract_Details_flag:
        time.sleep(1)
    callback.contract_Details_flag = False
    print callback.bond_ContractDetails_reqId    
    print callback.bond_ContractDetails.__dict__    
    
    
    
    
    
    # Market Depth #######################################################################
    # reqMktDepth          --->   updateMktDepth        self.update_MktDepth
    #                      --->   update_MktDepthL2     self.update_MktDepthL2
    ###################################################################################'''     
    print "Testing Market Depth Group \n"
    contract_info9 = create.create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')
    tws.reqMktDepth(7000, contract_info9, 3)
    time.sleep(5)
    print callback.update_MktDepth
    tws.cancelMktDepth(7000)





    # News Bulletin ######################################################################
    # reqNewsBulletins     --->   updateNewsBulletin    self.update_NewsBulletin_msgId
    #                                                   self.update_NewsBulletin_msgType
    #                                                   self.update_NewsBulletin_message
    #                                                   self.update_NewsBulletin_origExchange
    ###################################################################################'''     
    print "Testing News Bulletin Group \n"
    tws.reqNewsBulletins(1)
    time.sleep(20)
    tws.cancelNewsBulletins()





    # Financial Advisors Group ###########################################################
    # reqManagedAccts      --->   managedAccounts       self.managed_Accounts
    ###################################################################################'''     
    print "Testing Financial Advisors Group \n"
    tws.reqManagedAccts()    
    #tws.requestFA()       # non FA account. Unable to test.
    

    

    

    # Historical Data ####################################################################
    # reqHistoricalData    --->   historicalData        self.historical_Data
    ###################################################################################'''        
    print "Testing Historical Data Group \n"
    contract_Details10 = create.create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')    
    data_endtime = datetime.now().strftime("%Y%m%d %H:%M:%S")
    tws.reqHistoricalData(9000, contract_Details10, data_endtime,
                          "1 M", "1 day", "BID", 0, 1)
    time.sleep(3)
    tws.cancelHistoricalData(9000)

    
    
    
    
    # Market Scanners ####################################################################
    # reqScannerParameters --->   scannerParameters     self.scanner_Parameters
    #                      --->   scannerData           self.scanner_Data
    #                      --->   scannerDataEnd        self.scanner_Data_End_reqID    
    #                                                   self.scanner_Data_reqID  
    ###################################################################################'''        
    print "Testing Market Scanners Group \n"
    subscript = ScannerSubscription()
    subscript.numberOfRows(3)
    subscript.locationCode('STK.NYSE')
    tws.reqScannerSubscription(700, subscript)
    tws.reqScannerParameters()        
    time.sleep(3)
    tws.cancelScannerSubscription(700) 

    


    
    # Real Time Bars #####################################################################
    # reqRealTimeBars      --->   realtimeBar           self.real_timeBar
    ###################################################################################'''   
    print "Testing Real Time Bars Group \n"
    contract_Details11 = create.create_contract('EUR', 'CASH', 'IDEALPRO', 'USD')    
    tws.reqRealTimeBars(10000, contract_Details11, 5, "MIDPOINT", 0)
    time.sleep(10)
    tws.cancelRealTimeBars(10000)

    
    
    
    
    # Fundamental Data ###################################################################
    # reportType = ReportSnapshot
    #              ReportsFinSummary
    #              ReportsFinSummary
    #              ReportRatios
    #              ReportFinStatements
    #              RESC
    #              Calendar Report
    # Unfortunately, no access. 430, 'We are sorry, but fundamentals data for the 
    # security specified is not available.Not allowed'
    ###################################################################################'''     
    '''print "Testing Fundamental Data Group \n"
    contract_info12 = create.create_contract('AAPL', 'STK', 'SMART', 'USD')
    reportType = "ReportSnapshot"
    tws.reqFundamentalData(10100, contract_info12, reportType)
    time.sleep(10)
    tws.cancelFundamentalData(10100)'''


    

    
    # Disconnect from TWS
    time.sleep(2)
    tws.isConnected()
    tws.eDisconnect()
