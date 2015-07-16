# Bitcoin-Trading-Terminal
A simple but handy bitcoin trading terminal for geeks. 

#Usage(Commands):

Setting Trading Amount

	A<playing amount in 1/1000>[enter]
	
		A100[enter] -> set trading amount to 100/1000=0.1BTC
		
Trading Command:
 
	S|B|[enter]
	
	B|M|+|<price offset>|[enter]
	
	 |H|-|<price offset>|[enter]
	 
	Char 1
	
		S: Sell
		
		B: Buy
		
	Char 2
	
		B: Best bid/ask price
		
		M: Market price
		
		H: Half price in the threading
		
	Char 3
	
		+/-<price offset>
		
		Adjust your bid/ask price by offset in percentage
		
			e.g.: +100 = Original price + ( 100 / 100 ) = 1CNY
			
	Then press enter, and happy trading!
