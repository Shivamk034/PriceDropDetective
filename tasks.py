import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PriceDropDetective.settings")
django.setup()

import schedule,time,random
from scraper import *
from main.models import Product,Price,Track
from email_utils import send_email,get_template_price_drop_email
from django.urls import reverse
from dotenv import load_dotenv
load_dotenv()



def getScrapper(url):
    if("amazon" in url.lower()):
        return AmazonScrapper(url)
    elif("flipkart" in url.lower()):
        return FlipkartScrapper(url)
    else:
        return None

# 6(6+3),12(12+3),18(18+3),21(21+3) 
# 9,15,21,24 

def my_scheduled_job():
  # time.sleep(random.randint(15*60,3*60*60))  # random interval scrape intervals
  print("Started Scrapping")
  products = Product.objects.all()
  for i,product in enumerate(products):
    # time.sleep(random.randint(5,10))  # random interval between requests
    print(f"Scrapping {i+1}th url out of {len(products)} urls!")
    try:
      scrapper = getScrapper(product.url)
      product_price=scrapper.getPrice()
      if(product_price!=None):
        last_price = product.price_set.last()   # last scrapped price for this product
        if not Price.isValidPrice(product_price):
           raise Exception(f"invalid price :{product_price}")  
        
        price = Price(price=product_price,product=product)
        price.save()
        
        # check if price dropped
        print("price check")
        if(price.floatPrice() <= last_price.floatPrice()):
          # send email
          print("inside if block")
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
        print("couldn't scrap price of product id & title:",product.id,product.title)
         
    except Exception as e:
      print("Error while scrapping product id & title:",product.id,product.title)
      print(e)
  
  print("Scrapping Finished")



# schedule.every(int(os.environ["SCRAPING_INTERVAL"])).minutes.do(my_scheduled_job)
schedule.every(1).minutes.do(my_scheduled_job)
while True:
  schedule.run_pending()
  time.sleep(1)