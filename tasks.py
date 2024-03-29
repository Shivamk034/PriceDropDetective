import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PriceDropDetective.settings")
django.setup()

import schedule,time
from scraper.scraper import *
from main.models import Product,Price,Track
from email_utils import send_email,get_template_price_drop_email
from django.urls import reverse
from dotenv import load_dotenv
load_dotenv()



def getScrapper(driver,url):
    if("amazon" in url.lower()):
        return AmazonScrapper(driver,url)
    elif("flipkart" in url.lower()):
        return FlipkartScrapper(driver,url)
    else:
        return None


def my_scheduled_job():
  
  driver = getDriver()

  print("Started Scrapping")
  products = Product.objects.all()
  for i,product in enumerate(products):
    print(f"Scrapping {i+1}th url out of {len(products)} urls!")
    try:
      scrapper = getScrapper(driver,product.url)
      product_price=scrapper.getPrice()
      if(product_price!=None):
        last_price = product.price_set.last()   # last scrapped price for this product
        price = Price(price=product_price,product=product)
        price.save()
        
        # check if price dropped
        if(price.floatPrice()<last_price.floatPrice()):
          # send email
          recipients = [track.user for track in product.track_set.all()]
          for user in recipients:
            template = get_template_price_drop_email(
               name=user.username,
               product_name=product.title,
               product_url=product.url,
               previous_price=last_price.price,
               new_price=price.price,
               product_detail_url=reverse("detail",kwargs={"id":product.id})
               )
            send_email(subject=template["subject"],body=template["body"],recipients=user.email)

      else:
        scrapper.takeScreenshot()
        print("couldn't scrap price of product id:",product.id)
         
    except Exception as e:
      print("Error while scrapping product id:",product.id)
      print(e)
  
  print("Scrapping Finished")



schedule.every(int(os.environ["SCRAPING_INTERVAL"])).minutes.do(my_scheduled_job)
while True:
  schedule.run_pending()
  time.sleep(1)