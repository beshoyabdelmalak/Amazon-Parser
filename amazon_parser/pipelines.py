#import pymysql
from datetime import datetime
from elasticsearch import Elasticsearch
from amazon_parser.items import AmazonScrapItem
from amazon_parser.review import Review
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

class AmazonCrawlerPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, AmazonScrapItem):
            return self.handle_product(item,spider)
        if isinstance(item, Review):
            return self.handle_review(item, spider)


    def handle_product(self, item, spider):
      try:
          if item["productTitle"] != None and item["price"] != None and item['processorBrand'] != None and item['brandName'] != None and item['chipsetBrand'] != None and item['hardDriveType'] != None and item['ram'] != None:
              e = {"asin": item["asin"], "productTitle": str(item["productTitle"]), "price": float(item["price"]), "screenSize": item['screenSize'],
                    "displayResolutionSize": (item['maxScreenResolution_X'], item['maxScreenResolution_Y']),
                   "processorSpeed": item['processorSpeed'],
                    "processorType": str(item['processorType']), "processorCount": item['processorCount'], "processorManufacturer": str(item['processorBrand']),
                    "ram": item['ram'], "brandName": str(item['brandName']), "hardDriveType": item['hardDriveType'], "hddSize": item['hddSize'], "ssdSize": item['ssdSize'], "graphicsCoprocessor": str(item['graphicsCoprocessor']),
                   "chipsetBrand": str(item['chipsetBrand']), "operatingSystem": item['operatingSystem'], "itemWeight": item['itemWeight'],
                    "averageBatteryLife": item['averageBatteryLife'],
                   "productDimension": (item['productDimension_X'], item['productDimension_Y'], item['productDimension_Z']),
                   "color": item['color'], "imagePath": item['imagePath'], "avgRating": item['avgRating'], "ratingCount": item['ratingCount']}

              es.index(index='laptops', doc_type='laptop', body=e, refresh=True)
      except Exception as e:
            f = open("error.txt", "a+")
            f.write("asin : "+item["asin"]+'\n'+repr(e)+"\n")
            # print(repr(e))


    def handle_review(self,item, spider):
        query = '{ "query": {"match": {"asin": "' + str(item['asin']) + '"}}}'
        result = es.count(index="laptops",body=query)
        count = result['count']
        if count > 0:
          e = {"asin": item["asin"], "review": str(item["review"]), "rating": float(item["rating"]),"title":str(item['title'])}
          es.index(index="reviews",doc_type='review',body= e)



    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    @staticmethod
    def convert_date(date_string):
        date_object = datetime.strptime(date_string, '%B %d, %Y')
        return date_object
