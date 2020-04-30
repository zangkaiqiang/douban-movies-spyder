# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class MovieItem(Item):
    subjectId = Field()
    name = Field()
    director = Field()
    screenwriter = Field()
    Starring = Field()
    type = Field()
    production_region = Field()
    Language = Field()
    release_date = Field()
    first_broadcast_date = Field()
    episode = Field()

    length = Field()
    aka = Field()
    imdb_link = Field()
    douban_score = Field()
    rating_numbers = Field()
    star5 = Field()
    star4 = Field()
    star3 = Field()
    star2 = Field()
    star1 = Field()
