import scrapy
from pymongo import MongoClient
import datetime

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    
    def __init__(self, start_url=None, *args, **kwargs):
        super(BooksSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url] if start_url else []

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"bookes-{page}.html"
        bookdetail = {}
        
        self.log(f"Saved file {filename}")
        
        cards = response.css(".product_pod")
        for card in cards:
            title = card.css("h3>a::text").get()
            
            rating = card.css(".star-rating").attrib["class"].split(" ")[1]
            
            image = card.css(".image_container img")
            image = image.attrib["src"].replace("../../../../media", "https://books.toscrape.com/media/")
            
            price = card.css(".price_color::text").get()
            
            availability = card.css(".instock.availability")
            if len(availability.css(".icon-ok")) > 0:
                inStock = True
            else:
                inStock = False
            
            self.insertToDb(page, title, rating, image, price, inStock)
    
    def insertToDb(self, page, title, rating, image, price, inStock):
        client = MongoClient("{YOUR MONGO DB URI}")
        db = client.Star_Scrapper
        
        collection = db[page]
        page_sliced = page.split("_")[0]
        doc = {
            "Type": page_sliced,
            "Title": title,
            "Rating": rating,
            "Image_Url": image,
            "Price": price,
            "inStock": inStock,
            "date": datetime.datetime.utcnow().strftime('%Y-%m-%d')
        }
        inserted = collection.insert_one(doc)
        return inserted.inserted_id
