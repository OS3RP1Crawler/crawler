#!/usr/bin/python

from pymongo import MongoClient

URI = 'mongouri'


class db():
    test_collection = "test"
    prod_collection = "production"
    """docstring for dbconnect"""
    def __init__(self, database="dataSet"):
        self.db = MongoClient(URI + "/")[database]
        pass

    #dataSet
    def connect(self, collection=prod_collection):
        return self.db[collection]

    def insert(self, document, collection=prod_collection):
        return self.db[collection].insert_one(document)
