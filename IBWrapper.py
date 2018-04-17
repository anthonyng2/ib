'''
Wrapper - Organised by groups. E.g., Accont and Portfolio group, Orders group etc
2016-01-31
Updated 20 Nov 2016 for Python 3.
Updated 5 Apr 2018 to include limit price
'''
from __future__ import print_function 
from ib.ext.EWrapper import EWrapper
from ib.ext.Contract import Contract
from ib.ext.ExecutionFilter import ExecutionFilter
from ib.ext.Order import Order

class IBWrapper(EWrapper):
    def initiate_variables(self):
        # Account and Portfolio
        setattr(self, "accountDownloadEnd_flag", False)
        setattr(self, "update_AccountTime", None)
        setattr(self, "update_AccountValue", [])
        setattr(self, "update_Portfolio", [])
        setattr(self, 'account_Summary', [])
        setattr(self, 'account_SummaryEnd_flag', False)       
        setattr(self, 'update_Position', [])
        setattr(self, 'positionEnd_flag', False)
        # Orders
        setattr(self, 'order_Status', [])
        setattr(self, 'open_Order', [])
        setattr(self, 'open_OrderEnd_flag', True)        
        # Market Data
        setattr(self, 'tick_Price', [])
        setattr(self, 'tick_Size', [])        
        setattr(self, 'tick_OptionComputation', [])
        setattr(self, 'tick_Generic', [])        
        setattr(self, 'tick_String', [])        
        setattr(self, 'tick_EFP', [])    
        setattr(self, 'tickSnapshotEnd_reqId', [])           
        setattr(self, 'tickSnapshotEnd_flag', False)   
        # Connection and Server
        setattr(self, 'connection_Closed', False)
        # Executions
        setattr(self, "exec_Details_reqId", [])
        setattr(self, "exec_Details_contract", [])
        setattr(self, "exec_Details_execution", [])
        setattr(self, "exec_DetailsEnd_flag", False)
        # Contract
        setattr(self, "contract_Details_flag", False)
        # Market Depth
        setattr(self, 'update_MktDepth', [])
        setattr(self, 'update_MktDepthL2', [])        
        # Historical Data
        setattr(self, 'historical_Data', [])
        setattr(self, 'historical_DataEnd_flag', False)
        # Market Scanners
        setattr(self, 'scanner_Data_End_flag', False)
        setattr(self, 'scanner_Data', [])
        # Real Time Bars
        setattr(self, 'real_timeBar', [])

        
        
            
        



    # Account and Portfolio ###################################################
    def updateAccountValue(self, key, value, currency, accountName):
        update_AccountValue = self.update_AccountValue
        update_AccountValue.append((key, value, currency, accountName))
        
    def updatePortfolio(self, contract, position, marketPrice, marketValue, 
                        averageCost, unrealizedPnL, realizedPnL, accountName):
        update_Portfolio = self.update_Portfolio
        update_Portfolio.append((contract.m_conId, contract.m_currency, 
                                 contract.m_expiry, contract.m_includeExpired,
                                 contract.m_localSymbol, contract.m_multiplier,
                                 contract.m_primaryExch, contract.m_right,
                                 contract.m_secType, contract.m_strike,
                                 contract.m_symbol, contract.m_tradingClass,
                                 position, marketPrice, marketValue,
                                 averageCost, unrealizedPnL, realizedPnL, 
                                 accountName))    
    
    def updateAccountTime(self, timeStamp):
        self.update_AccountTime = timeStamp
        
    def accountDownloadEnd(self, accountName=None):
        self.accountDownloadEnd_accountName = accountName
        self.accountDownloadEnd_flag = True

    def accountSummary(self, reqId=None, account=None, tag=None, value=None, 
                       currency=None):
        account_Summary = self.account_Summary
        account_Summary.append((reqId, account, tag, value, currency))
        
    def accountSummaryEnd(self, reqId):
        self.accountSummaryEnd_reqId = reqId
        self.account_SummaryEnd_flag = True
        
    def position(self, account, contract, pos, avgCost):
        update_Position = self.update_Position
        update_Position.append((account, contract.m_conId, contract.m_currency, 
                                contract.m_exchange, contract.m_expiry, 
                                contract.m_includeExpired, contract.m_localSymbol, 
                                contract.m_multiplier, contract.m_right, 
                                contract.m_secType, contract.m_strike, 
                                contract.m_symbol, contract.m_tradingClass,
                                pos, avgCost))

    def positionEnd(self):
        setattr(self, 'positionEnd_flag', True)



    
    
    




    # Orders ###################################################################
    def orderStatus(self, orderId, status, filled, remaining, avgFillPrice, 
                    permId, parentId, lastFillPrice, clientId, whyHeld):
        order_Status = self.order_Status
        order_Status.append((orderId, status, filled, remaining, avgFillPrice, 
                            permId, parentId, lastFillPrice, clientId, whyHeld))
 
    def openOrder(self, orderId, contract, order, orderState):
        open_Order = self.open_Order
        open_Order.append((orderId, contract, order, orderState))

    def openOrderEnd(self):
        setattr(self, 'open_OrderEnd_flag', True)

    def nextValidId(self, orderId):
        self.next_ValidId = orderId
        
    def deltaNeutralValidation(self, reqId, underComp):
        pass









    # Market Data ##############################################################
    def tickPrice(self, tickerId, field, price, canAutoExecute):
        tick_Price = self.tick_Price
        tick_Price.append((tickerId, field, price, canAutoExecute))

    def tickSize(self, tickerId, field, size):
        tick_Size = self.tick_Size
        tick_Size.append((tickerId, field, size))

    def tickOptionComputation(self, tickerId, field, impliedVol, delta, 
                              optPrice, pvDividend, gamma, vega, theta, 
                              undPrice):
        tick_OptionComputation = self.tick_OptionComputation
        tick_OptionComputation.append((tickerId, field, impliedVol, delta, 
                                       optPrice, pvDividend, gamma, vega, 
                                       theta, undPrice))

    def tickGeneric(self, tickerId, tickType, value):
        tick_Generic = self.tick_Generic
        tick_Generic.append((tickerId, tickType, value))
       
    def tickString(self, tickerId, field, value):
        tick_String = self.tick_String
        tick_String.append((tickerId, field, value))
        
    def tickEFP(self, tickerId, tickType, basisPoints, formattedBasisPoints, 
                impliedFuture, holdDays, futureExpiry, dividendImpact, 
                dividendsToExpiry):
        tick_EFP = self.tick_EFP
        tick_EFP.append((tickerId, tickType, basisPoints, formattedBasisPoints, 
                         impliedFuture, holdDays, futureExpiry, dividendImpact, 
                         dividendsToExpiry))

    def tickSnapshotEnd(self, reqId):
        self.tickSnapshotEnd_reqId = reqId        
        setattr(self, 'tickSnapshotEnd_flag', True)        

    def marketDataType(self, reqId, marketDataType):
        setattr(self, 'market_DataType', marketDataType)
        print("market_DataType" + str(self.market_DataType))










    # Connection and Server ####################################################
    def currentTime(self, time):
        self.current_Time = time

    def error(self, id=None, errorCode=None, errorString=None):
        #print id
        print([id, errorCode, errorString])

    def error_0(self, strval=None):
        print("error_0")

    def error_1(self, id=0, errorCode=None, errorMsg=None):
        print("error_1")

    '''def error_0(self, strval):
        pass

    def error_1(self, id, errorCode, errorMsg):
        pass'''

    def connectionClosed(self):
        self.connection_Closed = True        










    # Executions ###############################################################        
    def execDetails(self, reqId, contract, execution):
        self.exec_Details_reqId = reqId
        self.exec_Details_contract = contract
        self.exec_Details_execution = execution

    def execDetailsEnd(self, reqId):
        self.exec_DetailsEnd_reqId = reqId        
        setattr(self, "exec_DetailsEnd_flag", True)
        
    def commissionReport(self, commissionReport):
        self.commission_Report = commissionReport









    # Contract #################################################################        
    def contractDetails(self, reqId, contractDetails):
        self.contract_Details_reqId = reqId
        self.contract_Details = contractDetails

    def contractDetailsEnd(self, reqId):
        self.contract_DetailsEnd_reqId = reqId
        self.contract_Details_flag = True

    def bondContractDetails(self, reqId, contractDetails):
        self.bond_ContractDetails_reqId = reqId
        self.bond_ContractDetails = contractDetails









    # Market Depth #############################################################
    def updateMktDepth(self, tickerId, position, operation, side, price, size):
        update_MktDepth = self.update_MktDepth
        update_MktDepth.append((tickerId, position, operation, side, price, size))
        #df = pd.DataFrame(self.update_MktDepth, columns = ["tickerId", "position", 
        #                                                   "operation", "side", 
        #                                                   "price", "size"])
        
    def updateMktDepthL2(self, tickerId, position, marketMaker, operation, 
                         side, price, size):
        # I don't get any of this so I can't test it. Following are just place holders. 
        print("blah blah. You have L2 data!!!")
        update_MktDepthL2 = self.update_MktDepthL2
        update_MktDepthL2.append((tickerId, position, operation, side, 
                                  price, size))  









    # News Bulletin ############################################################
    def updateNewsBulletin(self, msgId, msgType, message, origExchange):
        # During the time I test this, I don't get anything. Can't verify. Sorry. 
        print("You get News!!!")
        self.update_NewsBulletin_msgId = msgId
        self.update_NewsBulletin_msgType = msgType
        self.update_NewsBulletin_message = message
        self.update_NewsBulletin_origExchange = origExchange









    # Financial Advisors #######################################################
    def managedAccounts(self, accountsList):
        self.managed_Accounts = accountsList

    def receiveFA(self, faDataType, xml):
        pass










    # Historical Data  #########################################################
    def historicalData(self, reqId, date, open, high, low, close, volume, 
                       count, WAP, hasGaps):
        historical_Data = self.historical_Data
        historical_Data.append((reqId, date, open, high, low, close, volume, 
                       count, WAP, hasGaps))      
        #df = pd.DataFrame(self.historical_Data, columns = ["reqId", "date", "open", 
        #                                                   "high", "low", "close", 
        #                                                   "volume", "count", "WAP", 
        #                                                   "hasGaps"])








    # Market Scanners  #########################################################
    def scannerParameters(self, xml):
        self.scanner_Parameters = xml
        
    def scannerData(self, reqId, rank, contractDetails, distance, benchmark, 
                    projetion, legsStr):
        scanner_Data = self.scanner_Data
        scanner_Data.append((reqId, rank, contractDetails, distance, benchmark, 
                    projetion, legsStr))

    def scannerDataEnd(self, reqId):
        self.scanner_Data_End_reqID = reqId
        self.scanner_Data_End_flag = True










    # Real Tume Bars ###########################################################
    def realtimeBar(self, reqId, time, open, high, low, close, volume, 
                    wap, count):
        real_timeBar = self.real_timeBar
        real_timeBar.append((reqId, time, open, high, low, close, volume, 
                             wap, count))
        #df = pd.DataFrame(self.real_timeBar, columns = ["reqId", "time", "open", "high", 
        #                                                "low", "close", "volume", "wap", 
        #                                                "count"])









    # Fundamental Data #########################################################
    def fundamentalData(self, reqId, data):
        print("Getting Fundamental Data Feed Through")
        self.fundamental_Data_reqId = reqId
        self.fundamental_Data_data = data
        
        
        
        
        
        
        
        
        
    # Display Groups #########################################################       
    def displayGroupList(self, reqId, groups):
        pass

    def displayGroupUpdate(self, reqId, contractInfo):
        pass





        



                          





       




    




        
        
        
        
        

    
    
    
# Create Contract
class contract():
    def create_contract(self, symbol, secType, exchange, currency,
                        right = None, strike = None, expiry = None,
                        multiplier = None, tradingClass = None, 
                        localSymbol = None, includeExpired=None):
        contract = Contract()
        contract.m_symbol = symbol
        contract.m_secType = secType
        contract.m_exchange = exchange
        contract.m_currency = currency
        contract.m_right = right
        contract.m_strike = strike
        contract.m_expiry = expiry
        contract.m_multiplier = multiplier
        contract.m_tradingClass = tradingClass
        contract.m_localSymbol = localSymbol
        contract.m_includeExpired = includeExpired
        return contract
        
    def create_order(self, account, orderType, totalQuantity, action, 
                     lmt_price=None):
        order = Order()
        order.m_account = account
        order.m_orderType = orderType
        order.m_totalQuantity = totalQuantity
        order.m_action = action
        if orderType == "LMT":
            order.m_lmtPrice = lmt_price
        return order
    
    def exec_filter(self, client_id, accountName, contract):
        filt = ExecutionFilter()
        filt.m_clientId = client_id
        filt.m_acctCode = accountName
        #filt.m_time = "20160122-00:00:00"
        filt.m_symbol = contract.m_symbol
        filt.m_secType = contract.m_secType
        filt.m_exchange = contract.m_exchange
        return filt    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
'''
openOrder contains the following fields:
        self.tmp = [orderId, contract.m_comboLegs,
                    contract.m_comboLegsDescrip,
                    contract.m_conId,
                    contract.m_currency,
                    contract.m_exchange,
                    contract.m_expiry,
                    contract.m_includeExpired,
                    contract.m_localSymbol,
                    contract.m_multiplier,
                    contract.m_primaryExch,
                    contract.m_right,
                    contract.m_secId,
                    contract.m_secIdType,
                    contract.m_secType,
                    contract.m_strike,
                    contract.m_symbol,
                    contract.m_tradingClass,
                    contract.m_underComp,
                    order.m_account,
                    order.m_action,
                    order.m_activeStartTime,
                    order.m_activeStopTime,
                    order.m_algoParams,
                    order.m_algoStrategy,
                    order.m_allOrNone,
                    order.m_auctionStrategy,
                    order.m_auxPrice,
                    order.m_basisPoints,
                    order.m_basisPointsType,
                    order.m_blockOrder,
                    order.m_clearingAccount,
                    order.m_clearingIntent,
                    order.m_clientId,
                    order.m_continuousUpdate,
                    order.m_delta,
                    order.m_deltaNeutralAuxPrice,
                    order.m_deltaNeutralClearingAccount,
                    order.m_deltaNeutralClearingIntent,
                    order.m_deltaNeutralConId,
                    order.m_deltaNeutralDesignatedLocation,
                    order.m_deltaNeutralOpenClose,
                    order.m_deltaNeutralOrderType,
                    order.m_deltaNeutralSettlingFirm,
                    order.m_deltaNeutralShortSale,
                    order.m_deltaNeutralShortSaleSlot,
                    order.m_designatedLocation,
                    order.m_discretionaryAmt,
                    order.m_displaySize,
                    order.m_eTradeOnly,
                    order.m_exemptCode,
                    order.m_faGroup,
                    order.m_faMethod,
                    order.m_faPercentage,
                    order.m_faProfile,
                    order.m_firmQuoteOnly,
                    order.m_goodAfterTime,
                    order.m_goodTillDate,
                    order.m_hedgeParam,
                    order.m_hedgeType,
                    order.m_hidden,
                    order.m_lmtPrice,
                    order.m_minQty,
                    order.m_nbboPriceCap,
                    order.m_notHeld,
                    order.m_ocaGroup,
                    order.m_ocaType,
                    order.m_openClose,
                    order.m_optOutSmartRouting,
                    order.m_orderComboLegs,
                    order.m_orderId,
                    order.m_orderRef,
                    order.m_orderType,
                    order.m_origin,
                    order.m_outsideRth,
                    order.m_overridePercentageConstraints,
                    order.m_parentId,
                    order.m_percentOffset,
                    order.m_permId,
                    order.m_referencePriceType,
                    order.m_rule80A,
                    order.m_scaleAutoReset,
                    order.m_scaleInitFillQty,
                    order.m_scaleInitLevelSize,
                    order.m_scaleInitPosition,
                    order.m_scalePriceAdjustInterval,
                    order.m_scalePriceAdjustValue,
                    order.m_scalePriceIncrement,
                    order.m_scaleProfitOffset,
                    order.m_scaleRandomPercent,
                    order.m_scaleSubsLevelSize,
                    order.m_scaleTable,
                    order.m_settlingFirm,
                    order.m_shortSaleSlot,
                    order.m_smartComboRoutingParams,
                    order.m_startingPrice,
                    order.m_stockRangeLower,
                    order.m_stockRangeUpper,
                    order.m_stockRefPrice,
                    order.m_sweepToFill,
                    order.m_tif,
                    order.m_totalQuantity,
                    order.m_trailStopPrice,
                    order.m_trailingPercent,
                    order.m_transmit,
                    order.m_triggerMethod,
                    order.m_volatility,
                    order.m_volatilityType,
                    order.m_whatIf,
                    orderState.m_commission,
                    orderState.m_commissionCurrency,
                    orderState.m_equityWithLoan,
                    orderState.m_initMargin,
                    orderState.m_maintMargin,
                    orderState.m_maxCommission,
                    orderState.m_minCommission,
                    orderState.m_status,
                    orderState.m_warningText]
'''    
