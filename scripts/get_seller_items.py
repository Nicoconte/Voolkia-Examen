import requests
import logging
import getopt
import sys
import os

from dotenv import *

sys.path.append('../')
from utils.auth import Auth

class SellerItems:
	def __init__(self, seller_id, site_id) -> None:
		self.__seller_id = seller_id
		self.__site_id = site_id
		self.__http = requests
		self.__base_url = "https://api.mercadolibre.com/"
		
		self.__access_token = Auth().get_access_token()
		self.__header = {"Authorization": f"Bearer {self.__access_token}"}

	def __get_category_name_by_id(self, category_id):
		endpoint = f"{self.__base_url}/categories/{category_id}"
		category_info = self.__http.get(endpoint, headers=self.__header)
		name = category_info.json()['name']

		return name

	def __write_item_log(self, name, items):
		file = None

		if items == None:
			raise Exception

		try:
			file = open(f"{os.getcwd()}/../dist/{name}.log", "w+", encoding="utf8")

			for item in items:
				
				category_id = item['category_id']
				category_name = self.__get_category_name_by_id(category_id)

				file.write(f"{item['id']}, {item['title']}, {item['category_id']}, {category_name}\n")

			print("Done!")

		except Exception as e:
			logging.error(f"Cannot write log file. Reason {str(e)}")
		
		finally:
			if file is not None:
				file.close()		

	def get_published_items(self):		
		for seller in self.__seller_id:
			print(seller)
			try:
				endpoint = f"{self.__base_url}/sites/{self.__site_id}/search?seller_id={seller}"	
				print("a ", endpoint)
				response = self.__http.get(endpoint, headers=self.__header)
				print("b ", response.json())
				items = response.json().get('results')
				print("c ", items)
				self.__write_item_log(f"items_from_{seller}", items)
			
			except:
				logging.error(f"Invalid seller id -> {seller}")

#https://developers.mercadolibre.com.ar/es_ar/items-y-busquedas#Obtener-items-de-los-listados-por-vendedor
def main(argv):
	seller_id = ""
	site_id = ""

	#Entrada por teclado
	if len(argv) <= 0:
		seller_id = input('Seller id: ').strip().split(",")
		site_id = input('Site id: ').strip()

		print(seller_id)
		seller_items = SellerItems(seller_id, site_id)
		seller_items.get_published_items()		

	#Entrada por argumento
	else:
		try:

			options = "ss:"
			long_options = ["seller=", "site="]
			
			arguments, values = getopt.getopt(argv, options, long_options)

			for currentArg, currentValue in arguments:

				if currentArg in ('--seller'):
					seller_id = currentValue.split(",")

				elif currentArg in ('--site'):
					site_id = currentValue
				
				else:
					logging.warning("Invalid arg")

			seller_items = SellerItems(seller_id, site_id)
			seller_items.get_published_items()
		
		except Exception as e:
			logging.error(str(e))
			sys.exit(2)

if __name__ == "__main__":
	main(sys.argv[1:])