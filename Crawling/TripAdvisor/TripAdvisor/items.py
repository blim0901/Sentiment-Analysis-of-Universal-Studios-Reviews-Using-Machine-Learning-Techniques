# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TripadvisorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    a_docId = scrapy.Field()
    a_url = scrapy.Field()
    a_reviewer_name = scrapy.Field()
    a_reviewer_location = scrapy.Field()
    a_reviewer_contribution = scrapy.Field()
    a_comment_upvotes = scrapy.Field()
    a_comment_date = scrapy.Field()
    a_rating = scrapy.Field()
    a_title_comment = scrapy.Field()
    a_content_comment = scrapy.Field()
    
    pass
