import scrapy


class YatubeParsingItem(scrapy.Item):
    author = scrapy.Field()
    text = scrapy.Field()
    date = scrapy.Field()
