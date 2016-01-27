#!/usr/bin/python


class ShortUrlDoesNotExist(Exception):
    def __init__(self):
        Exception.__init__(self)
        self.str = "Short Url does not Exist"

    def __str__(self):
        return str(self.str)

class LongUrlDoesNotExist(Exception):
    def __init__(self):
        Exception.__init__(self)
        self.str = "Long Url does not Exist"

    def __str__(self):
        return str(self.str)
        