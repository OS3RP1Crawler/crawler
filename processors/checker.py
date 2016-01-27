#!/usr/bin/python


import re
import time
import socket

from urlparse import urlparse

import dns.resolver

GLOBAL_STRIP_REGEX = "(.*)\:.*"


class Checker(object):
    def __init__(self):
        pass
    
    @staticmethod
    def isAlive(long_url):
        hostname = Checker.getHostname(long_url)
        if Checker.isIP(hostname):
            return
        tries = 0
        while tries < 3:
            try:
                answer = dns.resolver.query(hostname)
                if len(answer) > 0:
                    return True
            except dns.resolver.NXDOMAIN, e:
                return False
            except Exception, e:
                print "Is Alive check Failed"
                tries += 1
                time.sleep(10)

        return False


    @staticmethod
    def isIP(ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

        
    @staticmethod
    def isHTTPS(long_url):
        url = urlparse(long_url)
        if url.scheme == 'https':
            return True
        else:
            return False
        
    @staticmethod
    def getHostname(long_url):
        stripped = urlparse(long_url)[1]
        hostname = re.search(GLOBAL_STRIP_REGEX, stripped)
        if hostname is None:
            return stripped
        else:
            return hostname.group(1)