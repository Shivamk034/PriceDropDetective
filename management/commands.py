from django.core.management.base import BaseCommand
from scraper.scraper import *
from main.models import Product,Price
import schedule,time

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
  for product,i in enumerate(products):
    print(f"Scrapping {i}th url out of {len(products)} urls!")
    try:
      scrapper = getScrapper(product.url)
      product_price=scrapper.getPrice()
      if(product_price!=None):
        price = Price(price=product_price,product=product)
        price.save()
    except:
      print("Error while scrapping product id:",product.id)
  
  print("Scrapping Finished")



class Command(BaseCommand):
  help = 'Prints all users'

  def handle(self, *args, **kwargs):
    schedule.every(1).minutes.do(my_scheduled_job)
    while True:
      schedule.run_pending()
      time.sleep(1)

