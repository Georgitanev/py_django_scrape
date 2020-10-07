"""Profiles"""

import os
import random
import sqlite3
from datetime import datetime

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy_jsonschema.item import JsonSchemaItem

from ..items import ParliamentPipeline

parties_dictionary = {
    "ПП ГЕРБ": "GERP",
    "БСП за БЪЛГАРИЯ": "BSP",
    "ВОЛЯ": "VOLQ",
    "Движение за права и свободи - ДПС": "DPS",
    "ОБЕДИНЕНИ ПАТРИОТИ - НФСБ, АТАКА и ВМРО": "OP",
}


class ProductItem(JsonSchemaItem):
    """ json schema to check jsons """

    jsonschema = {
        "$schema": "http://json-schema.org/schema#",
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "place_born": {"type": ["null", "string"]},
            "date_born": {"type": "string", "format": "date"},
            "profession": {"type": ["null", "string"]},
            "lang": {"type": ["null", "string"]},
            "party": {"type": "string"},
            "email": {"type": "string"},
            "fb": {"type": ["null", "string"]},
            "url": {"type": ["null", "string"]},
            "pp": {"type": "string"},
            "dob": {"type": "integer"},
        },
    }


def extract_date_place(date_born_place):
    """ extract date born and place born """
    start_date = date_born_place.find(": ") + 2
    end_date = start_date + 10
    date_born_scraped = date_born_place[start_date:end_date]
    date_born = datetime.strptime(date_born_scraped, "%d/%m/%Y").strftime("%Y-%m-%d")
    place_born = date_born_place[end_date + 1 :]
    if place_born == ", ":
        place_born = None
    if place_born == ", България":
        place_born = "България"
    return date_born, place_born


def parse_following_urls(response):
    """extracting 3 names, date and place of birth,
    profession, lang, party, e-mail, fb"""
    items = ParliamentPipeline()
    first_name = response.css("strong::text")[0].get()
    second_name = response.css(".MProwD::text").get()
    third_name = response.css("strong::text")[1].get()
    name = f"{first_name}{second_name}{third_name}"
    data = response.xpath("//div[4]/div[2]/div/ul/li/text()").getall()
    date_born, place_born = extract_date_place(data[0])
    lang_row = 2  # defining lang and party rows because some rows are
    # missing sometimes
    party_row = 3
    if data[1].startswith("Професия:"):
        profession = data[1][data[1].find(": ") + 2 : -1]
    else:
        profession = None
        lang_row -= 1
        party_row -= 1
    if data[lang_row].startswith("Езици:"):
        lang = data[lang_row][data[lang_row].find(": ") + 2 : -1]
    else:
        lang = None
        party_row -= 1
    if data[party_row].startswith("Избран"):
        party = data[party_row][data[party_row].find(": ") + 2 : -7]
        party = party.rstrip()
    try:
        email_href = response.xpath("//div[4]/div[2]/div/ul/li/a/@href").getall()[-1]
        if email_href.startswith("mailto:") is True:
            email = response.xpath("//div[4]/div[2]/div/ul/li/a/text()").getall()[-1]
            fb_href = None
        else:
            fb_href = response.xpath("//div[4]/div[2]/div/ul/li/a/@href").getall()[-1]
            if fb_href.startswith("https://www.facebook.com/"):
                fb_href = response.xpath("//div[4]/div[2]/div/ul/li/a/@href").getall()[
                    -1
                ]
                email = response.xpath("//div[4]/div[2]/div/ul/li/a/text()").getall()[
                    -2
                ]
    except BaseException as ex:  # if e-mail and fb_link are missing
        print(ex)
        email = None
        fb_href = None
    items["name"] = name
    items["date_born"] = date_born
    items["place_born"] = place_born
    items["profession"] = profession
    items["lang"] = lang
    items["party"] = party
    items["email"] = email
    items["fb"] = fb_href
    items["url"] = response.request.url[-11:]
    items["pp"] = parties_dictionary[party]  # political party short version
    items["dob"] = date_born.replace("-", "")  # date of birth short version
    yield items


class PostsSpider(scrapy.Spider):
    """ spyder who crawl"""

    name = "posts"
    allowed_domains = "parliament.bg"
    start_urls = ["https://www.parliament.bg/bg/MP/"]

    def parse(self, response):
        # parse any elements you need from the start_urls and, optionally,
        # store them as Items.
        # See http://doc.scrapy.org/en/latest/topics/items.html
        selector = Selector(response)
        urls_short = selector.xpath("//div[3]/div/div/div/a/@href").getall()
        # get unique from 2 different lists short_urls and links from DB
        path = os.path.dirname(os.path.abspath(__file__))
        db = os.path.join(path, "db.sqlite3")
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT url FROM Parliament1;")
        rows_urls = c.fetchall()
        rows = [i[0] for i in rows_urls]
        urls_short_unique = [i for i in urls_short if i not in rows]
        start_urls = [
            "https://www.parliament.bg" + short for short in urls_short_unique
        ]
        start_urls = start_urls[: random.randint(100, 140)]
        for url in start_urls:
            yield Request(url, callback=parse_following_urls, dont_filter=True)
