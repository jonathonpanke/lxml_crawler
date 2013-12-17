'''
 360pi Price Scraping Challenge

In any language and using any framework you feel comfortable with,
write a simple tool which will scrape the categories and products
from www.visions.ca, returning, at a minimum, the following information:
  -> The product categories available on the site
  -> At least one product from each category
  -> Each product's regular price
  -> Any sale or current price (if available)
  -> Do not do shipping or "in-cart" pricing

As a bonus (but not using these will not count against you), use:
  -> Python
  -> scrapy, lxml, or requests python libraries
  -> XPaths or CSS selectors
'''

from ProductItem import ProductItem
from Logger import Logger

from lxml import html
import requests


'''
A list of all the xpath strings that will be used in scraping the
www.visions.ca website. If the website were to change an aspect of
their html, quick changes can be done here instead of looking through
the code.
'''
root_url = "http://www.visions.ca"

xpath_categorylink = '//table[@class="parentMenuItem"]//tbody//tr//td//a/@href'
xpath_categoryname = '//div[@class="breadCrumbs"]//span//text()'

xpath_productlink = '//div[@class="productItemMain"]//div[2]//a/@href'
xpath_productname = '//h1[@class="seo_3_noMargin"]/text()'
xpath_productregprice = '//span[@class="regPrice"]//span/text()'
xpath_productsaleprice = '//span[@class="salePrice"]/text()'

'''
VisionCrawler is a class that is used to crawl and retreive data from
the web site www.visions.ca. The crawler will follo the specifications
of the above stated problem.
'''
class VisionsCrawler:

	'''
	The VisionCrawler class constructer creates an instance of the crawler
	needing one parameter, which is a logger. The logger needed is to put 
	the retreived data somewhere readable. 
	'''
	def __init__(self, logger):
		self.logger = logger

	'''
	Method retrieves the html links for the categories on the website.
	(Main category headings and not subcategories)

	Returns the html links in a list.
	'''
	def get_category_links(self):

		page = requests.get(root_url)
		tree = html.fromstring(page.text)

		category_links = tree.xpath(xpath_categorylink)

		return category_links

	'''
	Logs the category names from the given list of html links.
	'''
	def log_categories(self, category_links):

		self.logger.log("Product Categories \n\n")

		for link in category_links:

			page = requests.get(link)
			tree = html.fromstring(page.text)

			categoryname = tree.xpath(xpath_categoryname)
			category = "Category: " + categoryname[0] + "\n"
			self.logger.log(category)

		self.logger.log("\n")

	'''
	Logs the category name of a given category, using the link that
	is passed to the method.
	'''
	def log_categoryname(self, category_link):

		page = requests.get(category_link)
		tree = html.fromstring(page.text)

		categoryname = tree.xpath(xpath_categoryname)
		self.logger.log(categoryname[0] + "\n\n")

	'''
	Gets the list of product link on the webpage that the link 
	parameter accesses. 

	Returns the list of links for the webpage products.
	'''
	def get_product_list(self, category_link):

		page = requests.get(category_link)
		tree = html.fromstring(page.text)

		product_links = tree.xpath(xpath_productlink)

		# the format of the two retrieved links causes overlap
		# this string manipulation eliminates the overlap  
		delete_length = len(category_link) - 41
		category_link = category_link[:-delete_length]

		temp_list = []
		for plink in product_links:
			
			link = category_link + plink
			temp_list.append(link)

		return temp_list

	'''
	Retrieves the data from the given product link about the product.
	Gets the name of the product, the regular price and the sales price.
	From this data it creates a ProductItem and adds it to a list.

	Returns the list of ProductItems retrieved from the product links
	passed to the method.
	'''
	def get_product_info(self, product_links):
		
		item_list = []
		for link in product_links:

			page = requests.get(link)
			tree = html.fromstring(page.text)

			name = tree.xpath(xpath_productname)
			name = name[0] 

			price = tree.xpath(xpath_productregprice)
			if price: # if no price its instore only (so we ignore instore only) 
				price = price[0]

				sale_price = tree.xpath(xpath_productsaleprice)
				if not sale_price:
					sale_price = None
				else:
					sale_price = sale_price[0]

					# sale price always includes a 12 character string in front
					# of the price, this gets rid of the 12 characters
					sale_price = sale_price[12:] 

				item = ProductItem(name, price, sale_price)
				item_list.append(item)

		return item_list

	'''
	Logs the items from the given list to the logger file.
	'''
	def log_items(self, item_list):

		for item in item_list:
			self.logger.log(item)

	'''
	Runs the crawler to retrieve and log the product information fromstring
	www.visions.ca.
	'''
	def run_crawler(self):
		self.logger.create_log_file() # create a log file to log to

		# Get the links for the categories and then log them into
		# the log file
		category_links = self.get_category_links()
		self.log_categories(category_links)

		# Get the list of products from each category page
		for link in category_links:
	
			self.log_categoryname(link) # log the name of the current category

			product_links = self.get_product_list(link)
			product_list = self.get_product_info(product_links)

			self.log_items(product_list) # log the items


if __name__ == '__main__':
	logger = Logger("visions")
	crawler = VisionsCrawler(logger)
	crawler.run_crawler()