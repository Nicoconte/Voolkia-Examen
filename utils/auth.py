import webbrowser
import requests
import urllib
import os

from dotenv import *
from os import environ

class Auth:
	def __init__(self, dotenv_path=f"{os.getcwd()}/../config/.env"):
		load_dotenv(dotenv_path) #root folder
		
		self.__env_path = dotenv_path

		self.__http = requests
		self.__redirect_url = environ.get('REDIRECT_URI')
		self.__client_id = environ.get('APP_ID')
		self.__client_secret = environ.get('CLIENT_SECRET')

		self.__auth_code = None
		self.__auth_url = "http://auth.mercadolibre.com.ar"
		self.__full_auth_url = f"{self.__auth_url}/authorization?response_type=code&client_id={self.__client_id}&redirect_uri={self.__redirect_url}"

		self.__access_token = environ.get('ACCESS_TOKEN')

	def ask_for_auth_code(self):
		webbrowser.open(self.__full_auth_url)

	#Guarda o actualiza el access token dentro del archivo .env
	def append_access_token(self, token):
		file = open(self.__env_path, 'a+')
		
		#En caso de que la clave exista, la actualizamos 
		if "ACCESS_TOKEN" in file.read():
			environ['ACCESS_TOKEN'] = token
			file.close()
			return 

		#Sino lo creamos
		file.write(f'\nACCESS_TOKEN={token}')
		file.close()

	def get_access_token(self):

		if self.__access_token is not None:
			return self.__access_token

		#Esto es para un primer uso o una peticion del token (En caso de vencer)
		self.ask_for_auth_code()

		self.__auth_code = input('Introduce authorization code in order to get an access token (Copy after =): ')
		
		token_url = "https://api.mercadolibre.com/oauth/token"
	
		body = urllib.parse.urlencode({
			"grant_type": "authorization_code",
			"client_id": self.__client_id,
			"client_secret": self.__client_secret,
			"code": self.__auth_code,
			"redirect_uri": self.__redirect_url
		})

		header = {"content-type":"application/x-www-form-urlencoded"}

		response = self.__http.post(token_url, body, headers=header).json()

		access_token = response['access_token']

		self.append_access_token(access_token)

		return access_token
