import scrapy


class Review(scrapy.Item):
    asin = scrapy.Field()
    review = scrapy.Field()
    rating = scrapy.Field()
