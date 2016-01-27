#!/usr/bin/python
from filter.filter import Filter
from spamhaus.spamhaus import Spamhaus
from rp_google.safebrowse import SafeBrowse
from errors import ShortUrlDoesNotExist
from processors.processor import Processor
from processors.phishtank import Phishtank
from db.db import db
import threading
import time


class BaseService(threading.Thread):
    def __init__(self, filehandles, process_num):
        threading.Thread.__init__(self)
        self.handles = filehandles
        self.__entries_processed = 0
        self.__successful_entries = 0
        self.__exception_count = 0
        self.__retry_time = 5
        self.__active = True
        self.__process_num = process_num
        self.db = db()
        self.processor = Processor()
        self.spamhaus = Spamhaus()
        self.phishtank = Phishtank()

        self.user_agent = ("Mozilla/5.0 (X11; Linux x86_64)"
                           " AppleWebKit/537.36 (KHTML, like Gecko) "
                           "Chrome/47.0.2526.106 Safari/537.36")

    def getThreadNum(self):
        return self.__process_num

    def getURLs(self):
        #f = open("output/thread"+str(self.getThreadNum()), "w+")
        for handle in self.handles:
            for short_hash in handle:
                self.__entries_processed += 1
                # remove trailing newline
                if short_hash.endswith("\n"):
                    short_hash = short_hash[:-1]

                try:
                    long_url = self.getLongUrl(short_hash)

                    if long_url is not None:
                        self.__successful_entries += 1
                        if Filter(long_url).filterLongURL():
                            d = self.gatherData(long_url, short_hash)
                            self.db.insert(d)
                        else:
                            #filter did not pass
                            pass
                except ShortUrlDoesNotExist:
                    pass
                except BitlyError, e:
                    if str(e) == "RATE_LIMIT_EXCEEDED":
                        print "Rate limit"
                    else:
                        raise e
                except Exception as e:
                    #print e
                    pass


    def closeFiles(self):
        print "Closing files for thread", self.getThreadNum()
        for h in self.handles:
            h.close()

    def getLongUrl(self, short_hash):
        pass

    def getServiceID(self):
        pass

    def gatherData(self, long_url, short_hash):
        result = {}
        spamhaus = self.spamhaus.testLongURL(long_url)
        google = SafeBrowse.testLongURL(long_url)
        phishtank = self.phishtank.testLongURL(long_url)

        result['long_url'] = long_url
        result['short_hash'] = short_hash
        result['service'] = self.getService()
        result['service_id'] = self.getServiceID()

        result['malware_result'] = {}
        result['malware_result']['google'] = google
        result['malware_result']['spamhaus'] = spamhaus
        result['malware_result']['phishtank'] = phishtank

        if len(spamhaus) > 0 or google is not None or phishtank:
            result['malware'] = True
        else:
            result['malware'] = False

        result['short_url_metadata'] = self.getShortUrlMetadata(short_hash)
        result['long_url_metadata'] = self.processor.processLongUrl(long_url)

        return result

    def getShortUrlMetadata(self, short_hash):
        pass

    def getService(self):
        pass

    def run(self):
        data = []

        print "Starting process:", self.__process_num
        try:
            self.getURLs()
        except Exception as e:
            print "Exception detected on process:", self.__process_num
            print "Exception type:", type(e)
            print e
            print str(e)

            self.__exception_count += 1

            print "Putting process", self.__process_num, "to sleep for", self.__retry_time, "seconds."
            time.sleep(self.__retry_time)
            if self.__retry_time < 900:
                self.__retry_time *= 4
            else:
                self.__retry_time = 900

            try:
                self.__lock.release()
            except:
                pass
            print "Process", self.__process_num, "awake again."
            pass

        print "Ending process:", self.__process_num, "Entries processed:", self.__entries_processed, "Succesful entries:", self.__successful_entries
