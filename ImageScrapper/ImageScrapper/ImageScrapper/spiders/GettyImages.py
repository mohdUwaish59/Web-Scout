import scrapy
import pymongo
import datetime
from scrapy.http import Request

class GettyImagesSpider(scrapy.Spider):
    name = "GettyImages"
    allowed_domains = ["gettyimages.de"]

    def __init__(self, start_url=None, *args, **kwargs):
        super(GettyImagesSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url] if start_url else []

    def parse(self, response):
        #print(response.start_urls)
        date = datetime.datetime.now().strftime("%Y%m%d")
        db_name = "Getty_Images_Scrape"  # Set the default database name
        collection_name = response.url.split("/")[4].split("?")[0]
        collection_name = f"{collection_name}_{date}"
        
        # Extract image URLs using CSS selectors
        image_urls = response.css('a.TV1lZmIBFh_LgfiQqK1O figure picture img::attr(src)').extract()

        # Process the extracted image URLs and initiate downloads
        for url in image_urls:
            item = {'image_urls': [url]}
            self.insertToDb(item, db_name, collection_name)


    # MongoDB connection and data insertion function
    def insertToDb(self, item, db_name, collection_name):
        try:
            client = pymongo.MongoClient("")
            db = client[db_name]
            collection = db[collection_name]
            doc = dict(item)
            inserted = collection.insert_one(doc)
            print(f"Inserted item with _id: {inserted.inserted_id}")
        except Exception as e:
            print(f"Error inserting item: {str(e)}")
