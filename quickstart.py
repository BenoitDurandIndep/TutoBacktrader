from __future__ import (absolute_import, division, print_function, unicode_literals)
from matplotlib import dates
import datetime
import os.path
import sys

import backtrader as bt
import TestStrategy as strat

if __name__ == '__main__':
	cerebro = bt.Cerebro() #create cerebro entity

	#add strategy
	#cerebro.addstrategy(strat.TestStrategy)
	strats=cerebro.optstrategy(strat.TestStrategy,maperiod=range(10,31))

	#find the data file
	modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
	datapath = os.path.join(modpath,"./datas/orcl-1995-2014.txt")

	#create data feed
	data=bt.feeds.YahooFinanceCSVData(
		dataname=datapath,
		fromdate=datetime.datetime(2000,1,1),
		todate=datetime.datetime(2000,12,31),
		reverse=False
	)
	
	cerebro.adddata(data) #add the data feed  to cerebro

	cerebro.broker.setcash(100000.0)
	cerebro.addsizer(bt.sizers.FixedSize, stake=10)
	cerebro.broker.setcommission(commission=0.001)#0.1%

	#print(f"Starting Portfolio value:{cerebro.broker.getvalue()}")

	cerebro.run(maxcpus=1)

	#print(f"Final Portfolio value:{cerebro.broker.getvalue()}")

	#cerebro.plot()