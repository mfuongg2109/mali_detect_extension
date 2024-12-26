from dotenv import load_dotenv
import os
from urllib.parse import quote_plus
from Environment.path import dotenv_path
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv(dotenv_path)

username = quote_plus(os.environ.get('MONGODB_USER'))
password = quote_plus(os.environ.get('MONGODB_PWD'))

uri = f"mongodb+srv://{username}:{password}@maliwebdetect.8tzl3.mongodb.net/?retryWrites=true&w=majority&appName=MaliWebDetect"

client = MongoClient(uri, server_api=ServerApi('1'))

db = client['URLs']
collection = db['urls']
