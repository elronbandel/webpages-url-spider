# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from ..items import SpiderItem


def load_domains(path):
    with open(path) as f:
        return [x.strip() for x in f.readlines()]


class PagesSpider(CrawlSpider):

    name = 'pages'
    allowed_domains = load_domains("domains.csv")
    start_urls = ("http://" + domain for domain in allowed_domains)

    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse_items(self, response):
        item = SpiderItem()
        item['url'] = response.url
        return [item, ]


