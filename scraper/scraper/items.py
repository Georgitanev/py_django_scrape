# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class ParliamentPipeline(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    date_born = scrapy.Field()
    place_born = scrapy.Field()
    profession = scrapy.Field()
    lang = scrapy.Field()
    party = scrapy.Field()
    email = scrapy.Field()
    fb = scrapy.Field()
    url = scrapy.Field()
    pp = scrapy.Field()
    dob = scrapy.Field()
