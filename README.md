# ib Files

Released 1 Feb 2016

Updated 12 May 2016 with [Tutorial](https://nbviewer.jupyter.org/github/anthonyng2/ib/blob/master/IbPy%20Demo.ipynb)

* ib_class.py : Demonstrates how to call IB using IbPy for account and other information. The codes are intentionally kept in self contained groups. E.g., Account and Portfolio, Orders etc.
* IBWrapper.py : Wrapper functions to receive data from IB.

These codes have been tested on gateway Build 952.2f and TWS and **ONLY on paper trading account**. Please carry out your own test on your own account.It is best to be read in conjuction with the [IB Java API](http://interactivebrokers.github.io/tws-api/#gsc.tab=0) manual.

# IbPy - Interactive Brokers Python API
[IbPy](https://github.com/blampe/IbPy) was originally written by Troy Melhase.

IB TWS and Gateway can be obtained via [IB website](https://www.interactivebrokers.com.hk/en/index.php?f=16042)

# Introduction
[Interactive Brokers](https://www.interactivebrokers.com/en/index.php?f=14839&ns=T) offers a trading lab for education institution. 

The instructor receives a "master" account with the ability to view all the students account information. However, as our class size often varies from 20 to 40, extracting key information from each account can be tedious and time consuming. Hence the reason for turning to IB API and writing these codes. The students' Net Liquidation Value (NLV) are download automatically and posted to [plotly](https://plot.ly/)

It allows the students to view each others' NLV. Naturally, this encourages competition, learning and camaraderie as well as communication and sharing. You can find a sample notebook [here](http://nbviewer.jupyter.org/github/anthonyng2/ib/blob/master/FTC_NLV_Demo.ipynb)

The following example is a great way to start. However, if you are comfortable with Python and Pandas, you can check out this [Jupyter tutorial](https://nbviewer.jupyter.org/github/anthonyng2/ib/blob/master/IbPy%20Demo.ipynb)

# Example
Below is a sample code snippets for Account and Portfolio Group. Best to leave the portion prior to Account and Portfolio alone as it sets up the necessary state to receive information from IB.


        import time
        from datetime import datetime
        from IBWrapper import IBWrapper, contract
        from ib.ext.EClientSocket import EClientSocket
        from ib.ext.ScannerSubscription import ScannerSubscription
        
        if __name__=="__main__":
            callback = IBWrapper()                # Instantiate IBWrapper 
            tws = EClientSocket(callback)         # Instantiate EClientSocket
            host = ""
            port = 7496
            clientId = 5000
            tws.eConnect(host, port, clientId)    # Connect to TWS
            tws.setServerLogLevel(5)
            accountName = "DU123456"              # Make sure you use your own 
            create = contract()                   # Instantiate contract class
            
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
            ######################################################################################
            print "Testing Account and Portfolio \n"
            #tws.reqAccountUpdates(1, accountName)
            tws.reqAccountSummary(1,"All","NetLiquidation")
            #tws.reqPositions()
            time.sleep(2)

The following is the output

        Server Version: 76
        TWS Time at connection:20160202 09:33:21 SGT
        Testing Account and Portfolio 
        
        
        In [4]: callback.account_Summary
        Out[4]: 
        [(1, 'DI123456', 'NetLiquidation', '1012293.85', 'USD'),
         (1, 'DU123456', 'NetLiquidation', '803908.12', 'USD'),
        ...
         (1, 'DU123457', 'NetLiquidation', '831895.74', 'USD'),
         (1, 'DU123458', 'NetLiquidation', '1149361.71', 'USD'),
         (1, 'DU123459', 'NetLiquidation', '895145.61', 'USD'),
         (1, 'DU123460', 'NetLiquidation', '981381.33', 'USD')]


I'm very interested in your experience with the code. Please do drop me a note with any feedback you may have.

Anthony Ng


Look for me @ [https://www.algo-hunter.com](https://www.algo-hunter.com)
