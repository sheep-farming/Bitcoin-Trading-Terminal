'''
Huobi Bitcoin Trading Terminal

Command:

Setting Trading Amount
	A<playing amount in 1/1000>[enter]
		A100[enter] -> set trading amount to 100/1000=0.1BTC

Trading Command:
 
	S|B|[enter]
	B|M|+|<price offset>|[enter]
	 |H|-|<price offset>|[enter]

	Level 1
		S: Sell
		B: Buy
	Level 2
		B: Best bid/ask price
		M: Market price
		H: Half price in the threading
	Level 3
		+/-<price offset>
		Adjust your bid/ask price by offset in percentage
			e.g.: +100 = Original price + ( 100 / 100 ) = 1CNY


'''

#coding=utf-8

from Util import *
import subprocess
import threading #导入threading包
import os
import sys
import tty, termios
import HuobiService
from datetime import datetime
from time import sleep


PASSWORD='Your Trading Password Here'

defaultSellAmount=1
sell=0
buy=0

amounttp=defaultSellAmount
amount=round(amounttp/1000,3)
k=0
trading=0
text=''
stage=0
method=''
numvar=0
way=''
offset=0
comment='\n+Log'
def cls():
	subprocess.call('clear')

#cls()

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
new_settings = old_settings
#new_settings[3] = new_settings[3] & ~termios.ISIG
new_settings[3] = new_settings[3] & ~termios.ICANON
new_settings[3] = new_settings[3] & ~termios.ECHONL
termios.tcsetattr(fd,termios.TCSAFLUSH,new_settings)

def getch():
	fd = sys.stdin.fileno()
	ch = sys.stdin.read(1)
	return ch

def get():
	global text
	global stage
	global way
	global method
	global numvar
	global offset
	global amounttp
	global amount
	global comment
	global trading
	while(1):
		newchar=getch()
		if newchar=='=':
			newchar='+'
		if newchar.encode('utf')!=b'\x7f':
			if newchar.isdigit() or newchar.isalpha() or newchar==' ' or newchar=='.' or newchar=='+' or newchar=='-' :
				newchar=newchar.upper()
				if stage!=8:
					if len(text)>=3:
						if stage==3:
							if newchar.isdigit():
								text=text+newchar
								offsetnum=eval(text[3:len(text)])
								offset=round(pfix*offsetnum/100,2)

					if len(text)==2:
						if newchar=='+' or newchar=='-':
							if newchar=='+':
								pfix=1
							if newchar=='-':
								pfix=-1
							text=text+newchar
							stage=3
							offset=0



					if len(text)==1:
						if newchar=='M':
							text=text+newchar
							method=newchar
							if text[0]=='B':
								numvar=sell
							if text[0]=='S':
								numvar=buy
							stage=2
						if newchar=='H':
							text=text+newchar
							method=newchar
							stage=2
							numvar=round(((sell+buy)/2),2)
						if newchar=='B':
							text=text+newchar
							method=newchar
							if text[0]=='B':
								numvar=buy
							if text[0]=='S':
								numvar=sell
							stage=2
				if stage==8:
					if newchar.isdigit():
						text=text+newchar
						amounttp=float(text[1:len(text)])


				if len(text)==0:
					if newchar=='S' or newchar=='B' :
						text=text+newchar
						way=newchar
						stage=1
					if newchar=='A':
						text=text+newchar
						way=newchar
						stage=8

				

			if newchar.encode('utf')==b'\x03':
				text='QUIT'
				quit()
			if newchar.encode('utf')==b'\n':
				if stage==8 and len(text)>1:
					amount=round(amounttp/1000,3)
				if stage==2 or stage==3:
					p=round(offset+numvar,2)
					if way=='S':
						print(HuobiService.sell(1,str(p),amount,PASSWORD,None,SELL))
						comment=comment+'\n Sell'+str(amount)+'BTC at'+str(p)+'...'

					if way=='B':
						print(HuobiService.buy(1,str(p),amount,PASSWORD,None,BUY))
						comment=comment+'\n Buy'+str(amount)+'BTC at'+str(p)+'...'

					trading=1


				offset=0
				text=''
				stage=0
				method=''
				numvar=0
				way=''
				###Execution
		else:
			text=text[0:len(text)-1]
			if len(text)==0:
				stage=0
				method=''
				numvar=0
				way=''
				offset=0
			if stage!=8:
				
				if len(text)==1:
					stage=1
					method=''
					numvar=0
					offset=0
				if len(text)==2:
					stage=2
					offset=0

				if len(text)>3 and stage==3:
					offsetnum=eval(text[3:len(text)])
					offset=round(pfix*offsetnum/100,2)
				if len(text)==3 and stage==3:
					offset=0
			if stage==8:
				if len(text)==1:
					amounttp=0
				else:
					amounttp=float(text[1:len(text)])
		show(text,sell,buy,stage,way,method,numvar,amounttp,offset,comment) #b'\x7f'


def say():
	while(1):
		global k
		global sell
		global buy
		global numvar
		global trading
		price=HuobiService.getPrice()

		price=eval(price)
		ticker=price['ticker']
		sell=round(ticker['sell'],2)
		buy=round(ticker['buy'],2)
		if stage==2 or stage==3:
			if text[1]=='M':
				if text[0]=='B':
					numvar=sell
				if text[0]=='S':
					numvar=buy
			if text[1]=='H':
				numvar=round(((sell+buy)/2),2)
			if text[1]=='B':
				if text[0]=='B':
					numvar=buy
				if text[0]=='S':
					numvar=sell
		global comment
		ordStatus=HuobiService.getOrders(1,GET_ORDERS)
		k=k+1
		if str(ordStatus)=='[]' and trading==1 and k>=6:
			k=0
			trading=0
			comment=comment+'Done!'
		show(text,sell,buy,stage,way,method,numvar,amounttp,offset,comment)
		sleep(0.5)

		
def show(text,sell,buy,stage,way,method,numvar,amounttp,offset,comment):
	cls()
	print('\n Ask:'+str(sell)+ ' Bid:'+str(buy)+ ' Spread:' + str(round(sell-buy,2))+ ' Trading:' + str(amount)+'BTC ' + str(datetime.now().time())[0:12])
	print('\n ['+text+' '*(40-len(text))+']\n')
	if stage==8:
		amounttc=round(amounttp/1000,3)
		print('Change Trading Coin Amount to:\n'+str(amounttc))

	if stage!=8:
		if stage>=1:
			if way=='B':
				print(' Buy In,')
			if way=='S':
				print(' Sell Out,')
		if stage>=2:
			if method=='M':
				print(' Market Price, at\n '+str(numvar))
			if method=='H':
				print(' Half of Spread, at\n '+str(numvar))
			if method=='B':
				print(' Best Price, at\n '+str(numvar))
			numofd=numvar
		if stage==3:
			numofd=round((numvar+offset),2)
			print(' Price Offset:'+str(offset)+ ' at\n '+str(numofd))
		if stage==2 or stage==3:
			print('\n Total: \n CNY'+str(round(numofd*amount,2)))
	print(comment)

threads=[]
t1=threading.Thread(target=say)
threads.append(t1)
t2=threading.Thread(target=get)
threads.append(t2)
if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()

while(1):
	if(text=='QUIT'):
		quit()
	sleep(1)
