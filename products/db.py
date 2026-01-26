from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)
db = client["paws_and_claws"]

products_collection = db["products"]
cart_collection = db["cart"]



