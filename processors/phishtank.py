#!/usr/bin/python

from pymongo import MongoClient


class Phishtank():
    def __init__(self):
        connection = MongoClient("mongourl")
        self.db = connection["phishtank"]

    ''' Returns True on hit'''
    def testLongURL(self, url):
        result = self.db.entries.find({"url": url})
        return result.count() > 0
