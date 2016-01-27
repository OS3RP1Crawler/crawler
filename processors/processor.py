#!/usr/bin/python
'''
This Class does some general Processing of the URLs.
'''
import socket
import ssl
import requests

from lxml import html
from urlparse import urlparse
from processors.checker import Checker
from baseservice.errors import LongUrlDoesNotExist


class Processor():
    """docstring for Processor"""
    def __init__(self):
        self.user_agent = ("Mozilla/5.0 (X11; Linux x86_64)"
                           " AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/47.0.2526.106 Safari/537.36")
    
    def processLongUrl(self, long_url):
        data = {}
        url = urlparse(long_url)
        hostname = Checker.getHostname(long_url)
        
        if Checker.isAlive(long_url):
            certdata = ""
            if Checker.isHTTPS(long_url):
                certdata = ssl.get_server_certificate((hostname, url.port if url.port is not None else 443))
            headers = {'User-Agent': self.user_agent}
            response = requests.get(long_url, headers=headers)
            if response.status_code in [404, 402, 403]:
                raise LongUrlDoesNotExist()
            elif response is None:
                raise LongUrlDoesNotExist()
            elif response.status_code in [200]:
                data['cert'] = certdata

                data['header'] = {}
                data['header']['content-length'] = self.getHeader(response, 'content-length')
                data['header']['last-modified'] = self.getHeader(response, 'last-modified')
                data['header']['date'] = self.getHeader(response, 'date')
                data['header']['content-type'] = self.getHeader(response, 'content-type')

                data['script_links'] = self.parseHTML(response)
                data['alive'] = True



                return data

            else:
                raise Exception("Unknown status code "
                                + str(self.response.status_code) +
                                " for URL: " + long_url)
        else:
            data['alive'] = False
            return data

    def getHeader(self, response, str):
        if str in response.headers:
            return response.headers[str]
        else:
            return None

    def parseHTML(self,response):
        tree = html.fromstring(response.content)
        return tree.xpath('//script[@type="text/javascript"]/@src')
