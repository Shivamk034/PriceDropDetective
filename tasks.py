import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PriceDropDetective.settings")
django.setup()

import schedule,time
from scraper.scraper import *
from main.models import Product,Price

def getScrapper(url):
    if("amazon" in url.lower()):
        return AmazonScrapper(url)
    elif("flipkart" in url.lower()):
        return FlipkartScrapper(url)
    else:
        return None


def my_scheduled_job():
  
  print("Started Scrapping")
  products = Product.objects.all()
  for i,product in enumerate(products):
    print(f"Scrapping {i+1}th url out of {len(products)} urls!")
    try:
      scrapper = getScrapper(product.url)
      product_price=scrapper.getPrice()
      if(product_price!=None):
        price = Price(price=product_price,product=product)
        price.save()
      else:
        print("couldn't scrap price of product id:",product.id)
         
    except:
      print("Error while scrapping product id:",product.id)
  
  print("Scrapping Finished")



schedule.every(1).minutes.do(my_scheduled_job)
while True:
  schedule.run_pending()
  time.sleep(1)