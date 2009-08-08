#! /usr/bin/env python
""" Dump all links from all sitemaps found in a given index"""

import sys
import socks
import socket
sys.path = ['..'] + sys.path

from lxml.etree import XMLSyntaxError
import sitemap

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: ./dump-index.py index_url_or_path'
        sys.exit(1)

    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS4, "localhost", 9050)
    socket.socket = socks.socksocket

    index = sitemap.SitemapIndex.from_url(sys.argv[1], user_agent=agent)
    for set in index:
        try:
            for url in set:
                print url.loc
        except XMLSyntaxError:
            print >>sys.stderr, 'Failed download: %s' % set.source

