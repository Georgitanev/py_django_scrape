import scrapy
from typing import List, Optional, Dict, Union
import scrapy
from scrapy_jsonschema.item import JsonSchemaItem
# from genson import SchemaBuilder
from time import sleep
# from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from ..items import ParliamentPipeline
import sqlite3


# from scrapy.linkextractors.sgml import SgmlLinkExtractor
""" command to start
cd parliament
(scrapy crawl posts -o result.json -t json)
"""



"""
'name': name,
'date_born': date_born,
'place_born': place_born,
'profession': profession,
'lang': lang,
'party': party,
'email': email,
'fb': fb_href,
'data': data,
"""


class ProductItem(JsonSchemaItem):
    jsonschema: Dict[str, Union[str, Dict[str, Union[Dict[str, str], Dict[str, List[str]]]]]] = {
        '$schema': 'http://json-schema.org/schema#',
        'type': 'object', 'properties':
            {'name': {'type': 'string'},
             'place_born': {'type': ['null', 'string']},
             'date_born': {'type': 'string'},
             'profession': {'type': ['null', 'string']},
             'lang': {'type': ['null', 'string']},
             'party': {'type': 'string'},
             'email': {'type': 'string'},
             'fb': {'type': ['null', 'string']},
             'url': {'type': ['null', 'string']}}}
from datetime import datetime

# datetime.datetime.strptime("21/12/2008", "%d/%m/%Y").strftime("%Y-%m-%d")

def parse_following_urls(response):
    items = ParliamentPipeline()

    def extract_date_place(date_born_place):
        start_date = date_born_place.find(': ') + 2
        end_date = start_date + 10
        date_born_scraped = date_born_place[start_date:end_date]
        # date_born_scraped = '26/03/1967'
        date_born = datetime.strptime(date_born_scraped, "%d/%m/%Y").strftime("%Y-%m-%d")
        print(date_born)
        # 26/03/1967 convert to 1967-03-26
        # 1968-02-25
        place_born = date_born_place[end_date + 1:]
        if place_born == ', ':
            place_born = None
        if place_born == ', България':
            place_born = 'България'
        return date_born, place_born

    """ 3 names"""
    first_name = response.css('strong::text')[0].get()
    second_name = response.css('.MProwD::text').get()
    third_name = response.css('strong::text')[1].get()
    name = f'{first_name}{second_name}{third_name}'
    data = response.xpath('//div[4]/div[2]/div/ul/li/text()').getall()
    print('data12345', data)
    date_born, place_born = extract_date_place(data[0])
    """ profession, lang, party"""
    lang_row = 2
    party_row = 3
    if data[1].startswith('Професия:'):
        profession = data[1][data[1].find(': ') + 2:-1]
    else:
        profession = None
        lang_row -= 1
        party_row -= 1
    if data[lang_row].startswith('Езици:'):
        lang = data[lang_row][data[lang_row].find(': ') + 2:-1]
    else:
        lang = None
        party_row -= 1
    if data[party_row].startswith('Избран'):
        party = data[party_row][data[party_row].find(': ') + 2:-7]
        party = party.rstrip()

    """ e-mail and fb """
    try:
        email_href = response.xpath('//div[4]/div[2]/div/ul/li/a/@href').getall()[-1]
        if email_href.startswith('mailto:') is True:
            email = response.xpath('//div[4]/div[2]/div/ul/li/a/text()').getall()[-1]
            fb_href = None
        else:
            fb_href = response.xpath('//div[4]/div[2]/div/ul/li/a/@href').getall()[-1]
            if fb_href.startswith('https://www.facebook.com/'):
                fb_href = response.xpath('//div[4]/div[2]/div/ul/li/a/@href').getall()[-1]
                email = response.xpath('//div[4]/div[2]/div/ul/li/a/text()').getall()[-2]
    except Exception as ex:
        print(ex)
        email = None
        fb_href = None

    print("URL: " + str(response.request.url))
    items['name'] = name
    items['date_born'] = date_born
    items['place_born'] = place_born
    items['profession'] = profession
    items['lang'] = lang
    items['party'] = party
    items['email'] = email
    items['fb'] = fb_href
    items['url'] = response.request.url[-11:]
    yield items


class PostsSpider(scrapy.Spider):
    name = "posts"
    allowed_domains = 'parliament.bg'
    start_urls = ["https://www.parliament.bg/bg/MP/"]

    def parse(self, response):
        # parse any elements you need from the start_urls and, optionally, store them as Items.
        # See http://doc.scrapy.org/en/latest/topics/items.html

        s = Selector(response)
        urls_short = s.xpath('//div[3]/div/div/div/a/@href').getall()
        # get unique from two lists short and links from DB
        print('scraped urls number ', len(urls_short))
        conn = sqlite3.connect("D:\\git\\24_09_2019_download_repos\\py\\MyApi\\db.sqlite3")
        c = conn.cursor()
        c.execute("SELECT url FROM Parliament1;")
        rows_urls = c.fetchall()
        rows = [i[0] for i in rows_urls]
        print('All downloaded urls', rows_urls)
        urls_short_unique = [i for i in urls_short if i not in rows]
        print('unique_urls', urls_short_unique)
        start_urls = ['https://www.parliament.bg' + short for short in urls_short_unique]
        start_urls = start_urls[:80]
        # start_urls = start_urls
        print(start_urls)
        for url in start_urls:
            yield Request(url, callback=parse_following_urls, dont_filter=True)


# import json
# json_data = json.loads(open("data_export.json").read())

