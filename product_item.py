class product_item:

	def __init__(self, name, price, sales_price = None):
		self.name = name
		self.price = price
		self.sales_price = sales_price
		
	def __str__(self):
	
		if self.sales_price is None:
			return "Product: " + self.name + "\nPrice: " + self.price + "\n\n"
		else:
			return "Product: " + self.name + "\nPrice: " + self.price + "\nSale Price: " + self.sales_price + "\n\n"
