from product_item import product_item

from time import gmtime, strftime
from lxml import html
import requests

root_url = "http://www.visions.ca"
file_name = None

def scrape_root_page():

	create_log_file()

	page = requests.get(root_url)
	tree = html.fromstring(page.text)
	
	link = tree.xpath('//table[@class="parentMenuItem"]//tbody//tr//td//a/@href')

	scrape_products(link)
		
def scrape_products(list_links):
	
	for link in list_links:
	
		page = requests.get(link)
		tree = html.fromstring(page.text)
		
		category_name = tree.xpath('//div[@class="breadCrumbs"]//span//text()')
		category = "Category: " + category_name[0] + "\n"
		log(category)
		
		product_link = tree.xpath('//div[@class="productItemMain"]//div[2]//a/@href')
		product_link = product_link[0]
		
		
		url_length = 67
		delete_length = len(link) - url_length + 26
		link = link[:-delete_length]
	
		new_link = link + product_link
		
		scrape_product_info(new_link)		

def scrape_product_info(link):

	page = requests.get(link)
	tree = html.fromstring(page.text)
	
	name = tree.xpath('//h1[@class="seo_3_noMargin"]/text()')
	name = name[0]
	
	price = tree.xpath('//span[@class="regPrice"]//span/text()')
	if not price:
		price = "Instore Only"
	else:
		price = price[0]
	
	sales_price = tree.xpath('//span[@class="salePrice"]/text()')
	if not sales_price:
		sales_price = None
	else:
		sales_price = sales_price[0]
		sales_price = sales_price[12:]
	
	item = product_item(name, price, sales_price)
	
	log(item)
	
	
def log(item):

	f = open(file_name, "a")
	f.write(str(item))
	f.close()	

def create_log_file(log_number = 1):

	global file_name
	
	file_name = "log" + str(log_number) + ".txt"

	try:
		with open(file_name):
			create_log_file(log_number + 1)
	except IOError:
		f = open(file_name, "w")
		temp_string = "Log Time: " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\n\n"
		f.write(temp_string) 

if __name__ == '__main__':

	scrape_root_page()
