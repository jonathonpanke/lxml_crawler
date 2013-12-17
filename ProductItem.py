class ProductItem:

	'''
	ProductItem constructor, creates an instance of a product that
	has a name, a price, and sometimes a sale price.
	'''
	def __init__(self, name, reg_price, sale_price=None):

		self.name = name
		self.reg_price = reg_price
		self.sale_price = sale_price

	'''
	The override of the str() method.
	'''
	def __str__(self):

		if self.sale_price is None:
			return "Product: " + self.name + "\nPrice: " + self.reg_price + "\n\n"

		else:
			return "Product: " + self.name + "\nPrice: " + self.reg_price + "\nSale Price: " + self.sale_price + "\n\n"