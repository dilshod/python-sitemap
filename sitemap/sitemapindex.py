
from lxml import etree
from urllib2 import build_opener, Request
from cStringIO import StringIO

from urlset import *
from exceptions import *

class SitemapIndex(object):

    @staticmethod
    def from_url(url, user_agent='PythonSitemapParser/1.0', **kwargs):
        """ Create a sitemap from an url """
        request = Request(url)
        request.add_header('User-Agent', user_agent)
        opener = build_opener()
        kwargs['user_agent'] = user_agent
        return SitemapIndex(opener.open(request), url, **kwargs)

    @staticmethod
    def from_file(file, **kwargs):
        """ Create a sitemap from file """
        return SitemapIndex(open(file), file, **kwargs)

    @staticmethod
    def from_str(str, **kwargs):
        """ Create a sitemap from a string """
        return SitemapIndex(StringIO(str), 'string', **kwargs)

    source = property(lambda self:self._source)

    def __init__(self, handle, source='handle', validate=True, **kwargs):
        self._source = source
        self._handle = handle
        self._validate = validate
        self._kwargs = kwargs

    def get_urlsets(self):
        """ Parse the xml file and generate the urlsets. """
        if self._validate:
            schema = etree.XMLSchema(file=open(self.get_schema_path()))
        else:
            schema = None
        context = etree.iterparse(self._handle, events=('start',), schema=schema)

        location = ''
        for action, elem in context:
            tag = self._remove_ns(elem.tag)
            if tag == 'sitemap' and location:
                try:
                    yield UrlSet.from_url(location, validate=self._validate, **self._kwargs)
                except:
                    location = ''
                    continue
            elif tag == 'loc':
                location = elem.text
        del context
        del schema

    def _remove_ns(self, str):
        return re.sub('{[^}]*}', '', str)

    def get_schema_path(self):
        base = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base, 'schemas', 'siteindex.xsd')

    def __iter__(self):
        return iter(self.get_urlsets())

