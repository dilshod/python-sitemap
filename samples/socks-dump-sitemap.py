#! /usr/bin/env python
""" Dump all links from a sitemap """

import sys
import socks
import socket
sys.path = ['..'] + sys.path

import sitemap

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: ./dump-sitemap.py url_or_path'
        sys.exit(1)

    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, 'localhost', 9050)
    socket.socket = socks.socksocket

    set = sitemap.UrlSet.from_url(sys.argv[1])
    for url in set:
        print url.loc

