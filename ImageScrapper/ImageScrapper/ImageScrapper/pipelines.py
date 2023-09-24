# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ImagescrapperPipeline:
    def process_item(self, item, spider):
        return item
'''
import pymongo

class MongoDBPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, base_url,item, spider):
        # Get the collection name based on the spider name or URL
        #collection_name = spider.name  # You can use the spider name as a default
        collection_name = base_url.split('/')[3]  # Assuming the last part of the URL is the desired collection name
        collection_name = collection_name.split('?')[0]

        # Insert the item into the specified collection
        self.db[collection_name].insert_one(dict(item))
        return item'''

