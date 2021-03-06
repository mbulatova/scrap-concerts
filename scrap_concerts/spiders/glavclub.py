# -*- coding: utf-8 -*-
import scrapy
import json

from os.path import join, expanduser
from scrap_concerts.items import ScrapConcertsItem

class GlavclubSpider(scrapy.Spider):
    name = 'glavclub'
    allowed_domains = ['glavclub.com']
    start_urls = ['https://glavclub.com/#afisha']

    # Enable Feed Storage
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': join(expanduser('~'), "scrap-concert-results", "%(time)s.json")
    }

    def parse(self, response):
        for one in response.css(".posters-block script[type='application/ld+json'] ::text").extract():
            one_json = json.loads(one)

            url = one_json["url"]
            print("\n\n ------ ONE:\n", one_json)
            yield scrapy.Request(url, callback=self.get_description, meta={'item': {
                'date': one_json["startDate"],
                'name': one_json["name"]
            }})

    def get_description(self, response):
        item = response.meta['item']
        print('item = ', item)

        desc = response.css(".event-description-text").extract()
        item['description'] = desc

        short_url = response.css(".event-info-holder-image-big > img::attr(src)").extract_first()
        url = "https://" + self.allowed_domains[0] + short_url

        item['image_urls'] = [url]
        return item
