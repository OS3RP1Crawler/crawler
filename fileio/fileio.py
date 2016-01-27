"""
Crawler: FileIO class.

The FileIO class is used to read/write data on files
(thread status and script output).
"""


import os


class FileIO(object):
    def __init__(self, starting_point):
        pass

    @staticmethod
    def get_handles(dir):
        if not dir.endswith("/"):
            dir += "/"

        retlist = {}

        for filename in os.listdir(dir):
            retlist[filename] = open(dir + filename)
        return retlist
