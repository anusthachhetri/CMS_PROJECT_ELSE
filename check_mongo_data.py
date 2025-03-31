# check_mongo_data.py
from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['test']
collection = db['test']

# Find all documents
documents = collection.find()
for doc in documents:
    print(doc)
