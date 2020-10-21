import unittest
# import summarize
from pymongo  import MongoClient
import datetime
import random

class SummarizeTest(unittest.TestCase):


    def test_work_ng(self):
        pass

    def test_setup_work(self):
        db_name = "SewingMachine"
        collection_name = "WorkObjectDetection"

        client = MongoClient()

        db = client[db_name]
        db[collection_name].drop()
        collection = db[collection_name]

        session_id = "20200109163044181"

        dt = datetime.timedelta(milliseconds=100)
        timestamp = datetime.datetime.now()

        stamps = [ timestamp + (dt*i) for i in range(500)]

        data = list(map(lambda t: {"session_id": session_id,
                                   "timestamp": t.strftime("%Y%m%d%H%M%S%f")[:-3],
                                   "is_work": random.randint(1,1)}, stamps))

        result = collection.insert_many(data)

        find = collection.find()
        for doc in find:
            print(doc)


