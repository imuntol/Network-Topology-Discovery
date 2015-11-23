import pymongo
from pymongo import MongoClient
import datetime
client = MongoClient()
db = client['test']
collection = db['players']
print collection

#post = {"author": "Mike","text": "My first blog post!","tags": ["mongodb", "python", "pymongo"],"date": datetime.datetime.utcnow()}
#a = collection.insert_one(post).inserted_id
#print a

print collection.find_one()