#!/usr/bin/python


from bitlyretriever import BitlyRetriever
from baseservice.baseservice import BaseService
from datetime import datetime


class Bitly(BaseService):
    def __init__(self, filehandles, thread_num):
        BaseService.__init__(self, filehandles, thread_num)
        self.retriever = BitlyRetriever(self.user_agent)

    def getLongUrl(self, extention):
        return self.retriever.getLongUrl(extention)

    def getShortUrlMetadata(self, extention):
        clicks = self.retriever.getClicks(extention)
        referrers = self.retriever.getReferrers(extention)
        info = self.retriever.getInfo(extention)[0]

        data = {'created_at': Bitly.epoch_to_iso8601(info['created_at']),
                'total_clicks': clicks,
                'referrals': [],
                'created_by': info['created_by']}

        for domain, referrals in referrers.iteritems():
            c = 0

            for i in referrals:
                c += i['clicks']

            data['referrals'].append({u'count': str(c),
                                     u'id': domain})

        return data

    def getClicks(self, short_hash):
        return self.retriever.getClicks(short_hash)

    def getService(self):
        return "http://bit.ly/"

    def getServiceID(self):
        return 1

    @staticmethod
    def epoch_to_iso8601(timestamp):
        """
        epoch_to_iso8601 - convert the unix epoch time into
        a iso8601 formatted date
        >>> epoch_to_iso8601(1341866722)
        '2012-07-09T22:45:22'
        """
        return datetime.fromtimestamp(timestamp).isoformat()
