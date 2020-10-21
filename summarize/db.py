from aion.mongo import BaseMongoAccess
from pymongo import DESCENDING


class SummrizeCollection(BaseMongoAccess):

    def __init__(self, db_name, collection):
        self.collection = collection
        super().__init__(db_name)

    def find_equals_session_id(self, session_id):
        filter = {'session_id': {'$eq': session_id}}
        sort = [('timestamp', DESCENDING)]

        return self.find(self.collection, filter=filter, sort=sort)

    def find_one_latest_session_id(self):
        projection = {"_id": 0, "session_id": 1}
        sort = [('session_id', DESCENDING)]

        cur = self.find(self.collection,
                        projection=projection, sort=sort).limit(1)
        if cur.count():
            return cur.next().get('session_id')
        else:
            return None

    def create_indexes_summrize(self):
        self.create_index(self.collection, 'session_id', DESCENDING)
        self.create_index(self.collection, 'timestamp', DESCENDING)

    def insert_collection(self, data):
        return self.insert_one(self.collection, data)
