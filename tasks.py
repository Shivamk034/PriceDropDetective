import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PriceDropDetective.settings")
django.setup()
import schedule
import time
from utils.logger import logger
from scraper import AmazonScrapper, FlipkartScrapper
from main.models import Product, Price, Track
from email_module.brevo_api_client import send_email
from email_module.email_template import get_template_price_drop_email
from django.urls import reverse
from django.db import OperationalError, InterfaceError
from dotenv import load_dotenv
load_dotenv()

def get_scrapper(url):
    if "amazon" in url.lower():
        return None
    elif "flipkart" in url.lower():
        return FlipkartScrapper(url)
    else:
        return None

def process_product(product):
    try:
        scrapper = get_scrapper(product.url)
        
        if scrapper is None:
            logger.info(f"Skipping product with URL: {product.url}")
            return
        
        product_price = scrapper.getPrice()

        if product_price is not None:
            last_price = product.price_set.last()
            if not Price.isValidPrice(product_price):
                raise ValueError(f"Invalid price: {product_price}")

            price = Price(price=product_price, product=product)
            price.save()

            if price.floatPrice() <= last_price.floatPrice():
                recipients = [track.user for track in product.track_set.all()]
                for user in recipients:
                    template = get_template_price_drop_email(
                        name=user.username,
                        product_name=product.title,
                        product_url=product.url,
                        previous_price=last_price.price,
                        new_price=price.price,
                        product_detail_url=reverse("detail", kwargs={"id": product.id})
                    )
                    send_email(subject=template["subject"], body=template["body"], recipients=user.email)
        else:
            scrapper.takeScreenshot()
            logger.warning(f"Couldn't scrap price of product id & title: {product.id}, {product.title}")

    except InterfaceError as e:
        logger.error(f"Database interface error while scrapping product id & title: {product.id}, {product.title}")
        logger.exception(e)
    except OperationalError as e:
        logger.error(f"Database error while scrapping product id & title: {product.id}, {product.title}")
        logger.exception(e)
    except Exception as e:
        logger.error(f"Error while scrapping product id & title: {product.id}, {product.title}")
        logger.exception(e)
               
def my_scheduled_job():
    # interval = random.randint(15 * 60, 3 * 60 * 60)
    # logger.info(f"Sleeping for {interval} seconds before starting the scrape.")
    # time.sleep(interval)
    try:
        products = Product.objects.all()
        for product in products:
            if "amazon" not in product.url.lower():
                process_product(product)
    except Exception as e:
        logger.error("Error in the scheduler loop.")
        logger.exception(e)

schedule.every(int(os.environ["SCRAPING_INTERVAL"])).minutes.do(my_scheduled_job)

if __name__ == "__main__":
    while True:
        try:
            schedule.run_pending()
        except OperationalError as e:
            logger.error("OperationalError in the scheduler loop.")
            logger.exception(e)
        except InterfaceError as e:
            logger.error("InterfaceError in the scheduler loop.")
            logger.exception(e)
        except Exception as e:
            logger.error("Unexpected error in the scheduler loop.")
            logger.exception(e)
        time.sleep(1)