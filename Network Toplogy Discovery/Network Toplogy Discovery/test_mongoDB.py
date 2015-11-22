from pymongo import MongoClient
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['test']
collection = db['players']
a = collection.find_one()
print a
#posts = {"name":"sadasd","age":"221"}
#collection.insert_one(posts)

#print collection.find_one()
#for a in collection.find({"name": "Lionel Messi"}):
#    print a
#print client
#print "\n"
#print db
#print "\n"
#print collection
