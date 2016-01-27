#!/usr/bin/python


from tinyurlretriever import TinyurlRetriever
from baseservice.baseservice import BaseService


class Tinyurl(BaseService):
    def __init__(self, filehandles, thread_num):
        BaseService.__init__(self, filehandles, thread_num)
        self.retriever = TinyurlRetriever(self.user_agent)

    def getLongUrl(self, short_hash):
        return self.retriever.getLongUrl(short_hash)

    def getShortUrlMetadata(self, short_hash):
        return {}

    def getService(self):
        return "http://tinyurl.com/"

    def getServiceID(self):
        return 0
