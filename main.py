#!/usr/bin/python

import sys
import time

from bitly.bitly import Bitly
from rp_google.googl import Googl
from tinyurl.tinyurl import Tinyurl
from fileio.fileio import FileIO
from rp_google.safebrowse import SafeBrowse
#from retriever.baseretriever import BaseRetriever

# Now we can use the **Retriever classes :-)
# The magic is in the __init__.py file :)

# Some initial Variables
THREAD_NUMBER = 8
IP = "0.0.0.0"
PORT = 8008


def create_workers(service_obj, base_path):
    print "Creating workers..."
    worker_list = list()

    # if we use 8 threads, perhaps do ord(file_name) % 8 to divide work

    handles = FileIO.get_handles(base_path)
    divided_handles = {}

    print "Using", THREAD_NUMBER, "threads"

    for i in range(0, THREAD_NUMBER):
        divided_handles[i] = []

    for key, f in handles.iteritems():
        divided_handles[ord(key) % THREAD_NUMBER].append(f)


    for i in range(0, THREAD_NUMBER):
        s = service_obj(divided_handles[i], i)
        worker_list.append(s)

    print "Workers created."
    return worker_list


def start_workers(worker_list):
    print "Starting workers..."
    for worker in worker_list:
        worker.start()
    print "Workers started."


def stop_workers(worker_list):
    print "Stopping workers..."
    for worker in worker_list:
        worker.terminate()
    print "Workers stopped."


def join_workers(worker_list):
    print "Joining workers..."
    for worker in worker_list:
        worker.join()
    print "Workers joined."


def run(service, base_path):
    worker_list1 = create_workers(service, base_path)
    time.sleep(1)
    start_workers(worker_list1)

    join_workers(worker_list1)
    end_time = time.time()

    for worker in worker_list1:
        worker.closeFiles()

    #stop_workers(worker_list1)
    print "Ending time:", end_time
    print "Elapsed time:", end_time - start_time


if __name__ == "__main__":
    if not len(sys.argv) == 3:
        print "Usage: python main.py <service> <base path to urls>"
        sys.exit(1)

    print "Updating Google Safebrowsing List"
    #SafeBrowse.updateCache()

    service_to_use = sys.argv[1]
    base_path = sys.argv[2]

    start_time = time.time()
    print "Starting time:", start_time

    serviceObj = None
    if service_to_use == "bitly":
        run(Bitly, base_path)
    elif service_to_use == "tinyurl":
        run(Tinyurl, base_path)
    elif service_to_use == "googl":
        run(Googl, base_path)
    elif service_to_use == "all":
        for s in [Bitly, Tinyurl, Googl]:
            run(s, base_path)
