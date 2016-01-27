#!/usr/bin/python

import requests
from baseservice.errors import ShortUrlDoesNotExist
# http://tinyurl.com/zn6xdx9 --> os3.nl with redirects


class TinyurlRetriever():
    def __init__(self, useragent):
        self.short_url = ""
        self.response = None
        self.user_agent = useragent

    def getLongUrl(self, short_url):
        '''Returns the long URL the Tinyurl short_url points to.
        Unfortunately Tinyurl has no API so this is just following
        HTTP redirects'''
        r = self._get(short_url)

        return r.headers['location']

    def getLongUrlHeaders(self, short_url):
        r = self._get(short_url)
        return r.headers

    def _get(self, short_url):
        if self.short_url == short_url and self.response is not None:
            return self.response
        else:
            headers = {'User-Agent': self.user_agent}
            self.short_url = short_url
            try:
                self.response = requests.head("http://tinyurl.com/" + short_url,
                                              headers=headers)
                if self.response.status_code == 404:
                    raise ShortUrlDoesNotExist()
                elif self.response.status_code == 301:
                    return self.response
                elif self.response.status_code == 302:
                    return self.response
                else:
                    raise Exception("Unknown status code "
                                    + str(self.response.status_code) +
                                    " for URL: " + short_url)
            except Exception, e:
                pass
