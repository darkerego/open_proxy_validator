#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Darkerego, 2019
# Open Socks Proxy Validator

import requests
import threading
from random import shuffle
from time import sleep, time
from optparse import OptionParser
valid_proxies = []
verbose = False
very_verbose = False
print_content = False
global timeStamp


def print_writer(data):
    """
    :param data: data to write to file, called from check_proxy thread
    """
    global timeStamp
    ts = timeStamp
    with open('valid_proxy.' + str(ts) + '.lst', 'a') as f:
        data = str(data)
        print(data)
        f.write(data)


# TODO:  Create a class?
def check_proxies(proxy):
    """

    :param proxy: proxy to test
    """

    print('Testing %s' % proxy)
    try:
        resp = requests.get('https://ipecho.net/plain',
                              proxies=dict(http=proxy,
                                         https=proxy),
                            timeout=60)
    except Exception as err:
        if verbose:
            print('Invalid %s' % proxy)
        if very_verbose:
            print(err)
    else:
        if very_verbose or print_content:
            print(resp.content)
        if resp.status_code == 200:
            valid_proxies.append(proxy) # Future use
            print_writer(proxy+"\n")


def get_proxy_list(lst='pr.lst'):
    """

    :param lst: list from parse_list
    :return: an iterator via yield till list is done
    """
    proxies = []
    with open(lst, 'r') as p:
        p = p.readlines()
        for line in p:
            line_ = line.rstrip('\n')
            proxies.append(line_)
            # print(proxies)
        print('Shuffling...')
        shuffle(proxies)
        for i in proxies:
            yield(i)


def parse_list(proxy_lst):
    """

    :param proxy_lst: List of proxies in format: 1.21.146.255:9001:socks4
    :return: list of proxies in example format socks5://81.21.146.255:9001
    """
    p = get_proxy_list(proxy_lst)
    for i in p:
        x = str(i)
        proxy = x.split(':')
        host = proxy[0]
        port = proxy[1]
        ptype = proxy[2]
        proxy_: str = ptype + str('://') + host+":" + str(port)
        # proxy_ = str(proxy_)
        print('Trying %s' % proxy)
        tcount = threading.active_count()
        print('Active threads: %s' % tcount)
        if tcount < 1000:
            t = threading.Thread(target=check_proxies, args=(proxy_,))  # start a thread
            t.start()
        else:
            sleep(0.25)
            print('Wait...')
    print('Completed!')



def main():
    global verbose
    global very_verbose
    global print_content
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-f", "--proxy_lst", dest="filename",
                      help="read proxies from FILENAME", default='proxy.lst')
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("-d", "--very_verbose",
                      action="store_true", dest="very_verbose", help='Debug / Very Verbose mode')
    parser.add_option("-p", "--print_content", dest="print_content", help='Print html content from requests',
                      action='store_true')
    (options, args) = parser.parse_args()
    if len(args) > 1:
        parser.error("incorrect number of arguments")
    if options.filename:
        proxy_lst = options.filename
    if options.verbose:
        print('Verbose mode enabled')
        print("reading %s..." % options.filename)
        verbose = True
    if options.very_verbose:
        print('Very verbose mode enabled.')
        very_verbose = True
    if options.print_content:
        print('Will print content')
        print_content = True
    global timeStamp

    ts: str = time()
    timeStamp = str(ts)
    print('Program start at %s' % timeStamp)
    parse_list(proxy_lst)


if __name__ == "__main__":
    main()

