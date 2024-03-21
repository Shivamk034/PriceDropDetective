import requests
from bs4 import BeautifulSoup
import random
from abc import ABC, abstractmethod 
from selenium import webdriver


chrome_options = webdriver.ChromeOptions() # Create object ChromeOptions()
# chrome_options.add_argument('--headless')           
chrome_options.add_argument('--no-sandbox')                             
chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument("--log-level=3")
driver= webdriver.Chrome(options=chrome_options) # Create driver


def getSoup(url):
    
    driver.get(url)
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    return soup


class BaseScrapper(ABC):
    def __init__(self,url):
        self.soup = getSoup(url)

    def updateUrl(self,url):
        self.soup = getSoup(url)

    @abstractmethod
    def getPrice(self):
        pass
    
    @abstractmethod
    def getTitle(self):
        pass
    
    @abstractmethod
    def getImage(self):
        pass



def error_handler(f):
    def exec(*args,**kwargs):
        try:
            return f(*args,**kwargs)
        except Exception as e:
            print(e)

    return exec

class AmazonScrapper(BaseScrapper):
    def __init__(self,url):
        super().__init__(url)
    
    @error_handler
    def getTitle(self):
        return self.soup.find('span',{'id':'productTitle'}).text.strip()
    
    @error_handler
    def getPrice(self):
        return self.soup.find("div", {'id': "corePriceDisplay_desktop_feature_div"}).find("div", {"class": "a-section"}).find("span",{"class":"a-price"}).text
        # return self.soup.find("form",{"id":"addToCart"}).find("span",{"class":"a-price"}).find("span").text
        #return self.souperySelector("form#addToCart span.a-price span")find("form",{"id":"addToCart"}).find("span",{"class":"a-price"}).find("span").text
        
    @error_handler
    def getImage(self):
        return self.soup.find("div",{"id":"imgTagWrapperId"}).find("img",{"id":"landingImage"}).attrs["src"]
        
    def getData(self):
        return {
            "title":self.getTitle(),
            "price":self.getPrice(),
            "image":self.getImage(),
        }

class FlipkartScrapper(BaseScrapper):
    def __init__(self,url):
        super().__init__(url)
    
    @error_handler
    def getTitle(self):
        return self.soup.find("span",{'class': 'B_NuCI'}).text
        
    @error_handler
    def getPrice(self):
        return self.soup.find('div', {'class' : '_25b18c'}).find('div', {'class' : '_30jeq3'}).text
    
    @error_handler
    def getImage(self):
        return self.soup.find("div",{"class":"_3kidJX"}).find("img").attrs['src']
        
    def getData(self):
        return {
            "title":self.getTitle(),
            "price":self.getPrice(),
            "image":self.getImage(),
        }

if __name__ == "__main__":
    # https://www.amazon.in/dp/B07WHQRN1B/
    # https://www.flipkart.com/p/itm3b20cdb30cb02
    scrapper = AmazonScrapper("https://www.amazon.in/iQOO-Storage-Snapdragon%C2%AE-Platform-Flagship/dp/B07WHQRN1B/ref=sr_1_1?crid=19L7NK8R9STI6&dib=eyJ2IjoiMSJ9.OyUzPuZTCZl1GjdKSaEht0L5iHqOCtl-qUqVHjB6KPDI9zLiFSc5VmT34CHkKQINfBf94NApKuzWo2QoyxKLUPRH6ecxpW7VAC3hSLCIzpH4TBInhWvEuCckhzZIXE3kKFrX6WO-KNV9OQCFFzTzqBYHao8lJwwAZWlgCHrELQEpsi_OGMyFishmbm58St43Z4IC7kgfuqq6pXMNEhplkRczJe6YdFxoUzUO-Jyo0r8.k0Z4BCtCDigPS7Jmk1eXUxUlkC15zJqnaoD6FUZA_8U&dib_tag=se&keywords=iqoo%2B12%2Bpro&qid=1709395711&sprefix=iq%2Caps%2C228&sr=8-1&th=1")
    # scrapper = FlipkartScrapper('https://www.flipkart.com/sti-printed-men-round-neck-white-black-t-shirt/p/itm3b20cdb30cb02?pid=TSHGU4KZKMHZ75TZ&lid=LSTTSHGU4KZKMHZ75TZIQFLW0&marketplace=FLIPKART&q=tsgirt&store=clo%2Fash%2Fank&spotlightTagId=BestsellerId_clo%2Fash%2Fank&srno=s_1_3&otracker=search&otracker1=search&fm=Search&iid=3e35c42e-3955-4e82-aa28-c33989a3cc19.TSHGU4KZKMHZ75TZ.SEARCH&ppt=sp&ppn=sp&ssid=n2l1kptmxc0000001709397145260&qH=8d2cb22c633b1858')
    open("index.html","w").write(scrapper.soup.prettify())
    print(scrapper.getData())

    scrapper.updateUrl("https://www.amazon.in/dp/B0CHM745CT/ref=syn_sd_onsite_desktop_0?ie=UTF8&pd_rd_plhdr=t&aref=94rDEQyVIg&th=1")
    print(scrapper.getData())

    scrapper = FlipkartScrapper('https://www.flipkart.com/sti-printed-men-round-neck-white-black-t-shirt/p/itm3b20cdb30cb02?pid=TSHGU4KZKMHZ75TZ&lid=LSTTSHGU4KZKMHZ75TZIQFLW0&marketplace=FLIPKART&q=tsgirt&store=clo%2Fash%2Fank&spotlightTagId=BestsellerId_clo%2Fash%2Fank&srno=s_1_3&otracker=search&otracker1=search&fm=Search&iid=3e35c42e-3955-4e82-aa28-c33989a3cc19.TSHGU4KZKMHZ75TZ.SEARCH&ppt=sp&ppn=sp&ssid=n2l1kptmxc0000001709397145260&qH=8d2cb22c633b1858')
    print(scrapper.getData())
