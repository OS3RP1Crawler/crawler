#!/usr/bin/python
'''
Categorize From Spamhaus
'''
import re
from processors.checker import Checker

import dns.resolver


GLOBAL_STRIP_REGEX = "(.*)\:.*"

class Spamhaus():
    def __init__(self):
        pass

    def testLongURL(self,long_url):
        ip = ""
        hostname = Checker.getHostname(long_url)
        if Checker.isIP(hostname):
            ip = hostname.split('.')
        else:
            try:
                answer = dns.resolver.query(hostname, "A")
                for data in answer:
                    ip = data.address.split('.')
            except Exception, e:
                print e

        try:
            answer = dns.resolver.query(ip[3] + "." + ip[2] + "." + ip[1] + "." + ip[0] + ".zen.spamhaus.org", "A")
            self._categorize(answer)
        except dns.resolver.NXDOMAIN, e:
            return []
        except Exception:
            return []
        

    def _categorize(self,lookup):
        result = []
        for data in lookup:
            if data.address == "127.0.0.2":
                result.append("SBL Advisory")
            elif data.address == "127.0.0.3":
                result["spamhaus"].append("CSS Advisory")
            elif data.address == ("127.0.0.4" or "127.0.0.5" or "127.0.0.6" or "127.0.0.7"):
                result["spamhaus"].append("XBL Advisory")
            elif data.address == ("127.0.0.10" or "127.0.0.11"):
                result["spamhaus"].append("PBL Advisory")
        return result


