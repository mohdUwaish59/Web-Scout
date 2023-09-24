import scrapy
import pymongo
import datetime

client = pymongo.MongoClient("mongodb+srv://Mohd_Uwaish_Scrapy:QzcG8c9LOMWoqeHp@cluster0.olcx7kr.mongodb.net/")
db = client.Getty_Images_Scrape

def insertToDb(item, db_name, collection_name):
    try:
        db = client[db_name]
        collection = db[collection_name]
        doc = dict(item)
        inserted = collection.insert_one(doc)
        print(f"Inserted item with _id: {inserted.inserted_id}")
    except Exception as e:
        print(f"Error inserting item: {str(e)}")

class GettyImagesSpider(scrapy.Spider):
    name = "GettyImages"
    allowed_domains = ["gettyimages.de"]

    # Define the URL pattern with a placeholder for the page number
    base_url = "https://www.gettyimages.de/fotos/car?assettype=image&license=rf&alloweduse=availableforalluses&family=creative&phrase=Car&sort=mostpopular&page={}"

    def start_requests(self):
        # Start scraping from page 1
        yield scrapy.Request(url=self.base_url.format(1), callback=self.parse)

    def parse(self, response):
        date=datetime.datetime.now().strftime("%Y%m%d")
        db_name = "Getty_Images_Scrape"  # Set the default database name
        collection_name = response.url.split("/")[4].split("?")[0]
        collection_name = f"{collection_name}_{date}"
        
        # Extract image URLs using CSS selectors
        image_urls = response.css('a.TV1lZmIBFh_LgfiQqK1O figure picture img::attr(src)').extract()

        # Process the extracted image URLs and initiate downloads
        for url in image_urls:
            item = {'image_urls': [url]}
            insertToDb(item, db_name, collection_name)

        # Extract the total number of pages
        current_page = int(response.css('input[data-testid="search-pagination-input"]::attr(value)').get())
        total_pages = int(response.css('span.JO4Dw2C5EjCB3iovKUcw::text').get())

        # Generate URLs for the next pages and follow them
        if current_page < 1:
            next_page = current_page + 1
            next_url = self.base_url.format(next_page)
            yield scrapy.Request(next_url, callback=self.parse)
