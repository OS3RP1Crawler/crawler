#!/usr/bin/python

from baseservice.baseservice import BaseService
import requests
from baseservice.errors import ShortUrlDoesNotExist
import time


class Googl(BaseService):
    API_KEY = ["YOURKEYS"]

    def __init__(self, filehandles, thread_num):
        BaseService.__init__(self, filehandles, thread_num)
        self.short_hash = ""
        self.meta_short_hash = ""
        self.last_fetch = 0
        self.metadata = None
        self.response = None

    def getLongUrl(self, short_hash):
        r = self._get(short_hash)
        if 'longUrl' in r:
            return r['longUrl']
        else:  # rate limiting :<
            raise Exception(r)

    def getShortUrlMetadata(self, short_hash):
        r = self._get(short_hash)
        data = {'created_at': r['created'],
                'created_by': 0,  # non-existant for Goo.gl
                'referrals': r['analytics']['allTime']['referrers'],
                'total_clicks': r['analytics']['allTime']['shortUrlClicks'],
                # google only
                'status': r['status']
                }

        return data

    def _get(self, short_hash):
        if self.short_hash == short_hash and self.response is not None:
            return self.response.json()
        else:
            headers = {'User-Agent': self.user_agent}
            self.meta_short_hash = short_hash

            curtime = time.time()
            if int(curtime - self.last_fetch) <= 1:
                time.sleep(curtime - self.last_fetch)

            self.last_fetch = curtime
            try:
                self.response = requests.get(self._getEndpoint(short_hash),
                                             headers=headers)

                if self.response.status_code in [404]:
                    raise ShortUrlDoesNotExist()
                return self.response.json()
            except Exception, e:
                pass

    def _getEndpoint(self, short_hash):
        if self.getThreadNum() is not None:
            return ("https://www.googleapis.com/urlshortener/v1/url"
                    "?projection=FULL&key="
                    + self.API_KEY[self.getThreadNum()] +
                    "&shortUrl=http://goo.gl/"
                    + short_hash)
        else:
            raise Exception("Thread num not set")

    def getService(self):
        return "http://goo.gl/"

    def getServiceID(self):
        return 2
