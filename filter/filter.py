#!/usr/bin/python
import re
from urlparse import urlparse


class Filter(object):

    GLOBAL_FILTER_HTTP = "^https?:\/\/.*"
    GLOBAL_FILTER_CREDS = ("(sess(ion|id|ionid)?=)|"
                           "(u(=|ser(name)?|name)?=)|"
                           "(pass(wd|word)?=)")
    GLOBAL_HTTP_AUTH = "^((.*):(.*))@"

    """docstring for LongUrlFilterer"""
    def __init__(self, long_url):
        self.url = urlparse(long_url)

    """Returns True when URL may be analyzed """
    def filterHTTP(self):
        return (self.url.scheme == "http" or self.url.scheme == "https")

    ''' Returns True when URL may be analyzed '''
    def filterPrivacy(self):
        m = re.search(self.GLOBAL_FILTER_CREDS, self.url.query)
        return m is None

    '''Returns true when URL may be analyzed'''
    def filterHTTPAuth(self):
        result = re.search(self.GLOBAL_HTTP_AUTH, self.url.netloc)
        return result is None  # no matches, so can analyze

    """Returns True when URL may be analyzed"""
    def filterLongURL(self):
        methods = [self.filterHTTP, self.filterPrivacy, self.filterHTTPAuth]
        result = True
        for m in methods:
            result = result and m()

        return result
