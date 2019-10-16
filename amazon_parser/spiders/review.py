# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy import Selector

from amazon_parser.review import Review


class ReviewSpider(scrapy.Spider):
    name = 'review'
    start_urls = []

    for file in os.listdir("review_xml_files"):
      if str(file) == ".DS_Store":
        continue
      start_urls.append(
        "file://" + os.path.realpath("review_xml_files") + "/" + str(file))  # replace with your local path


    def parse(self, response):
      sel = Selector(text=response.body)
      reviews_ratings = self.getReviews(sel)
      if reviews_ratings:
        for i in range(len(reviews_ratings[0])):
          review = Review()
          review['review'] = reviews_ratings[0][i]
          review['rating'] = reviews_ratings[1][i]
          review['title'] = reviews_ratings[2][i].strip()
          review['asin'] = self.getAsin(sel)
          yield review

    def getReviews(self, sel):
      reviews = sel.xpath(
          '//*[contains(concat( " ", @class, " " ), concat( " ", "review-text-content", " " ))]//span').extract()
      new_reviews= []
      if reviews :
          for review in reviews:
            review = review.replace("<br>", ".")
            review = review.replace('<span class="">'," ")
            review = review.replace("</span>","")
            new_reviews.append(review)
          # print(len(new_reviews))
          # print(new_reviews)
          crawled_ratings = sel.xpath(
              '//*[(@id = "cm_cr-review_list")]//*[contains(concat( " ", @class, " " ), concat( " ", "a-icon-alt", " " ))]/text()').extract()
          ratings = []
          titles = sel.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "a-text-bold", " " ))]//span/text()').extract()
          # print(len(titles))
          for rating in crawled_ratings:
            rating = float(rating[:rating.find('out of 5 stars') - 1].strip())
            ratings.append(rating)
          reviews_rating = [new_reviews, ratings, titles]
          result = zip(reviews_rating[2], reviews_rating[1])
          resultSet = set(result)
        #   print(resultSet)
          return reviews_rating
      else:
        return None

    def getAsin(self,sel):
      asin = sel.xpath("//div[@class='asin']/text()").get()
      return asin
