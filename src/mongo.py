import pymongo

class Database:
    def __init__(self, name, client=pymongo.MongoClient()):
        self.name = name
        self.client = client
        self.db = self.client[self.name]
        self.cols = {}

    def addCol(self, colname):
        self.cols[colname] = self.db[colname]

    def insertRecord(self, colname, record):
        _id = self.cols[colname] = record
        return _id
