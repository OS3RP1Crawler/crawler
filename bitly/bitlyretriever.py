'''
This Class Handles all api calls towards bitly
'''

import bitly_api
import requests
from baseservice.errors import ShortUrlDoesNotExist


API_KEY = "APIKEY"


class BitlyRetriever():
    def __init__(self, useragent):
        self.user_agent = useragent
        self.short_url = ""
        self.response = None
        self.connection = None

    def getLongUrl(self, extention):
        r = self._get(extention)

        return r.headers['location']

    def getReferrers(self, extention):
        connection = self._setupconnection()
        link_referrers_by_domain = connection.link_referrers_by_domain(link=self._makeshorturl(extention))
        if u'error' in link_referrers_by_domain:
            if link_referrers_by_domain[u'error'] == u'NOT_FOUND':
                raise ShortUrlDoesNotExist()
            else:
                pass
        else:
            return link_referrers_by_domain

    def getClicks(self, extention):
        connection = self._setupconnection()

        try:
            clicks = connection.link_clicks(self._makeshorturl(extention))
            return clicks
        except bitly_api.BitlyError as e:
            if e.message == "NOT_FOUND":
                raise ShortUrlDoesNotExist()
            else:
                raise e
            return None

    def getInfo(self, extention):
        connection = self._setupconnection()
        try:
            info = connection.info(shortUrl=self._makeshorturl(extention))
            if 'error' in info[0] and info[0]['error'] == "NOT_FOUND":
                raise ShortUrlDoesNotExist()
            return info
        except bitly_api.BitlyError as e:
            if e.message == "NOT_FOUND":
                raise ShortUrlDoesNotExist()
            else:
                raise e


    def _setupconnection(self):
        if self.connection is None:
            self.connection = bitly_api.Connection(access_token=API_KEY)

        return self.connection

    def _makeshorturl(self, extention):
        return "http://bit.ly/" + extention

    def _get(self, short_url):
        if self.short_url == short_url and self.response is not None:
            return self.response
        else:
            headers = {'User-Agent': self.user_agent}
            self.short_url = short_url
            try:
                self.response = requests.head(self._makeshorturl(short_url),
                                              headers=headers)

                if self.response.status_code in [404, 402, 403]:
                    raise ShortUrlDoesNotExist()
                elif self.response.status_code in [301, 302]:
                    return self.response
                else:
                    raise Exception("Unknown status code "
                                    + str(self.response.status_code) +
                                    " for URL: " + short_url)
            except Exception, e:
                pass
