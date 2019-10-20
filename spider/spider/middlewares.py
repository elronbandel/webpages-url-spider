# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from urllib.parse import urlparse
from collections import defaultdict
from scrapy.exceptions import IgnoreRequest
from tldextract import extract

class FilterDomainbyLimitMiddleware(object):
    def __init__(self, limit):
        self.limit = limit
        self.visiteds = set()
        self.counter = defaultdict(int)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('REQ_PER_DOMAIN_LIMIT'))

    def extract_domain(self, url):
        extracted = extract(url)
        return "{}.{}".format(extracted.domain, extracted.suffix)

    def limited(self, domain):
        return self.counter.get(domain, 0) > self.limit

    def visited(self, url):
        return url in self.visiteds

    def visit(self, url):
        self.visiteds.add(url)

    def count(self, domain):
        self.counter[domain] += 1

    def printer(self, domain):
        print("domain: {} reached: {}".format(domain, self.counter[domain]))

    def process_request(self, request, spider):

        url = request.url
        domain = self.extract_domain(request.url)

        if self.visited(url):
            return None
        self.visit(url)

        if self.limited(domain):
            raise IgnoreRequest()

        self.count(domain)
        return None
