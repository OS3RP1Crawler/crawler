#!/usr/bin/python

from gglsbl import SafeBrowsingList

GOOGLE_SAFEBROWSE_API_KEY = ("AIzaSyBHwcXIygLEaNAPwFYxL-lVQiQJqa5KE3s")


class SafeBrowse():
    def __init__(self):
        pass

    @staticmethod
    def updateCache():
        sbl = SafeBrowsingList(GOOGLE_SAFEBROWSE_API_KEY ,  db_path="/opt/crawler/gsb_v3.db")
        sbl.update_hash_prefix_cache()

    @staticmethod
    def testLongURL(long_url):
        sbl = SafeBrowsingList(GOOGLE_SAFEBROWSE_API_KEY, db_path="/opt/crawler/gsb_v3.db")
        return sbl.lookup_url(long_url)
