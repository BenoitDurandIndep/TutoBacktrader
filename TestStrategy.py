
import backtrader as bt

class TestStrategy(bt.Strategy):
	params=(
		("maperiod",15),
	)
	def log(self,txt,dt=None):
		#logging function
		dt=dt or self.datas[0].datetime.date(0)
		print(f"{dt.isoformat()} > {txt}")

	def __init__(self):
		#Keep a reference to the close line in the data[0] dataseries
		self.dataclose=self.datas[0].close
		
		#to keep track of pending orders
		self.order = None
		self.buyprice= None
		self.buycomm=None

		# Add SMA
		self.sma = bt.indicators.SMA(self.datas[0],period=self.params.maperiod)

	def notify_order(self, order):
		if order.status in [order.Submitted, order.Accepted]:
			return # Buy/Sell order submitted/accepted -> nothing to do

		#check if an order has been completed, broker could reject order if not enough cash
		if order.status in [order.Completed]:
			if order.isbuy():
				self.log(f"BUY EXECUTED price: {order.executed.price} cost : {order.executed.value:9.2f} comm : {order.executed.comm:9.2f}")
				self.buyprice = order.executed.price
				self.buycomm = order.executed.comm
			elif order.issell():
				self.log(f"SELL EXECUTED price : {order.executed.price} cost : {order.executed.value:9.2f} comm : {order.executed.comm:9.2f}")

			self.bar_executed = len(self)
		elif order.status in [order.Canceled, order.Margin, order.Rejected]:
			self.log(f"Order Canceled/Margin/Rejected")

		self.order = None #Write down : no pending order

	def notify_trade(self, trade):
		if not trade.isclosed:
			return
		self.log(f"OPERATION PROFIT gross {trade.pnl} net {trade.pnlcomm}")

	def next(self):
		#Simply log the closing price
		self.log(f"Close: {self.dataclose[0]}")

		if self.order: #check if an order is pending, if yes we exit
			return

		if  not self.position: #if we are not in the market

			#current close less than previous close
			# and previos close les than previous one
			if self.dataclose[0] > self.sma[0]:
				#BUY!
				self.log(f"BUY CREATE: {self.dataclose[0]}")
				self.buy()
		else: #already in the market, we might sell
			if self.dataclose[0] < self.sma[0]:
				# SELL !
				self.log(f"SELL CREATE:{self.dataclose[0]}")
				self.order=self.sell()
