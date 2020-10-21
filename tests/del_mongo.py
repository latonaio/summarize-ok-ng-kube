from  pymongo  import MongoClient

client = MongoClient()
db = client['SewingMachine']
collection = db['WorkObjectDetection']
cur = collection.find()
for doc in cur:
    print(doc)

collection.drop()
print("delete collection")


