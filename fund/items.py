# -*- coding: utf-8 -*-
import scrapy


class EastmoneyFundItem(scrapy.Item):
    code = scrapy.Field()
    initials = scrapy.Field()

    name = scrapy.Field()
    type = scrapy.Field()

    pinyin = scrapy.Field()
    net_worth = scrapy.Field()
