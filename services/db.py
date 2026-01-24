from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_URI)
db = client["paws_and_claws"]

# Services offered
services_collection = db["services"]

# Service bookings
bookings_collection = db["service_bookings"]
