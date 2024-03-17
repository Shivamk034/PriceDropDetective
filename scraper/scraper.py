from abc import ABC, abstractmethod 
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from pathlib import Path
import os
from datetime import datetime




ua = UserAgent()


log_dir=Path("logs/images/")
if not os.path.exists(log_dir): os.makedirs(log_dir)

def getOptions():
    chrome_options = webdriver.ChromeOptions() # Create object ChromeOptions()
    chrome_options.add_argument('--headless')           
    chrome_options.add_argument('--no-sandbox')                             
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--log-level=0")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # chrome_options.add_argument("--window-size=2220,1080")
    # chrome_options.add_argument(f"user-agent={ua.random}")
    return chrome_options

def getDriver():
    # Set up the Chrome driver
    driver = webdriver.Chrome(options=getOptions())
    driver.set_window_size(2220,1080)
    # driver.maximize_window()
    # close existing driver
    # if driver:  driver.close()
    return driver

class BaseScrapper(ABC):
    def __init__(self,driver,url):
        self.driver = driver
        self.updateUrl(url)

    # def __del__(self):
    #     print("Destructor called !")
    #     self.driver.close()

    @classmethod
    def getBaseUrl(cls,url):
        return "/".join(url.split("/",3)[:3])+"/"

    @classmethod
    def getShortUrl(cls,url):
        return url
    
    def updateUrl(self,url):
        self.url=url
        self.driver.get(url)
        cur_time = datetime.now()
        img_path = log_dir/Path(f"{cur_time.day}-{cur_time.month}-{cur_time.year}--{cur_time.hour}-{cur_time.minute}-{cur_time.microsecond}.png")
        self.driver.save_screenshot(img_path)

    def getHTML(self):
        return self.driver.page_source.encode("UTF-8")



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
    def __init__(self,driver,url):
        super().__init__(driver,url)

    @staticmethod
    def _get_asin(url):
        parts = url.split("/dp/",1)[-1].split("/",1)
        return parts[0] if isinstance(parts,list) else parts
    
    
    @classmethod
    def getShortUrl(cls,url):
        asin = cls._get_asin(url)
        return cls.getBaseUrl(url) + 'dp/' + asin
    
    @error_handler
    def getTitle(self):
        return self.driver.find_element(By.XPATH, '//*[@id="productTitle"]').text
    
    @error_handler
    def getPrice(self):
        
        base_selector=""".//div[@id="corePriceDisplay_desktop_feature_div" or @id="corePrice_desktop"]//div[contains(concat(" ",normalize-space(@class)," ")," a-section ")]//span[contains(concat(" ",normalize-space(@class)," ")," a-price ")]"""
        try:
            symbol= self.driver.find_element(By.XPATH,base_selector+'//span[contains(concat(" ",normalize-space(@class)," ")," a-price-symbol ")]').text
            whole= self.driver.find_element(By.XPATH,base_selector+'//span[contains(concat(" ",normalize-space(@class)," ")," a-price-whole ")]').text
            decimal= '.'
            fraction= self.driver.find_element(By.XPATH,base_selector+'//span[contains(concat(" ",normalize-space(@class)," ")," a-price-fraction ")]').text
            return symbol + whole + decimal + fraction
        except:
            return self.driver.find_element(By.XPATH, base_selector).text 
        
        
    @error_handler
    def getImage(self):
        return self.driver.find_element(By.XPATH, '//*[@id="landingImage"]').get_attribute('src')
        
    def getData(self):
        return {
            "title":self.getTitle(),
            "price":self.getPrice(),
            "image":self.getImage(),
        }

class FlipkartScrapper(BaseScrapper):
    def __init__(self,driver,url):
        super().__init__(driver,url)
    
    @classmethod
    def getShortUrl(cls,url):
        return url.split("?",1)[0]
    
    @error_handler
    def getTitle(self):
        # return self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div[1]/h1/span[2]').text
        return self.driver.find_element(By.CSS_SELECTOR,"span.B_NuCI").text

        
    @error_handler
    def getPrice(self):
        return self.driver.find_element(By.CSS_SELECTOR,"div._25b18c div._30jeq3").text

    
    @error_handler
    def getImage(self):
        return self.driver.find_element(By.CSS_SELECTOR,"div._3kidJX img").get_attribute("src")

        
    def getData(self):
        return {
            "title":self.getTitle(),
            "price":self.getPrice(),
            "image":self.getImage(),
        }

if __name__ == "__main__":
    # https://www.amazon.in/dp/B07WHQRN1B/
    # https://www.flipkart.com/p/itm3b20cdb30cb02
    # url = "https://www.amazon.in/dp/B07WHQRN1B/"
    driver = getDriver()

    
    url = "https://www.amazon.com/dp/B088SKYMF2/"
    scrapper = AmazonScrapper(driver,AmazonScrapper.getShortUrl(url))
    print(scrapper.url)
    print(scrapper.getData())
    
    driver.close()
    exit()

    url = "https://www.amazon.com/dp/B07PVCK9KX/"
    scrapper.updateUrl(AmazonScrapper.getShortUrl(url))
    print(scrapper.url)
    print(scrapper.getData())
    
    url = "https://www.amazon.com/dp/B07CNPBS7T/"
    scrapper.updateUrl(AmazonScrapper.getShortUrl(url))
    print(scrapper.url)
    print(scrapper.getData())

    # url = "https://www.amazon.com/Hope-Rainbow-Hoda-Kotb/dp/0593624122/?_encoding=UTF8&_encoding=UTF8&ref_=dlx_gate_sd_dcl_tlt_fa13649f_dt_pd_gw_unk&pd_rd_w=FPLOl&content-id=amzn1.sym.81a68cec-8afc-4296-99f7-78cf5ddc15b5&pf_rd_p=81a68cec-8afc-4296-99f7-78cf5ddc15b5&pf_rd_r=KAD1QPN234SH5MXYBNW6&pd_rd_wg=A7ZKi&pd_rd_r=fa39bbc3-93b1-41a2-b592-77d89dfc6566"
    # url = "https://www.amazon.in/Lux-Cozi-Melange-Regular-Sleeves/dp/B0CH9QMFF4/ref=sl_ob_desktop_dp_0_2_v2?_encoding=UTF8&pd_rd_w=1Bm0J&content-id=amzn1.sym.cdbcd11c-3329-43cb-9547-fb297b2c655b&pf_rd_p=cdbcd11c-3329-43cb-9547-fb297b2c655b&pf_rd_r=PTKWAM93FTVZKNGQFPVM&pd_rd_wg=iE7ky&pd_rd_r=ccfc3bd0-e267-435c-85d3-f63c78a1db0a"
    url = "https://www.amazon.in/dp/B0CHM745CT/ref=syn_sd_onsite_desktop_0?ie=UTF8&pd_rd_plhdr=t&aref=94rDEQyVIg&th=1"
    scrapper.updateUrl(AmazonScrapper.getShortUrl(url))
    print(scrapper.url)
    print(scrapper.getData())

    # url = 'https://www.flipkart.com/apple-iphone-15-blue-128-gb/p/itmbf14ef54f645d?pid=MOBGTAGPAQNVFZZY&lid=LSTMOBGTAGPAQNVFZZYO7HQ2L&marketplace=FLIPKART&store=tyy%2F4io&spotlightTagId=BestsellerId_tyy%2F4io&srno=b_1_1&otracker=browse&fm=organic&iid=fedd7fea-5ff7-4bd7-a5f0-a9008f1702c3.MOBGTAGPAQNVFZZY.SEARCH&ppt=browse&ppn=browse&ssid=7un6hxsq6o0000001710258321538'
    # scrapper = FlipkartScrapper(driver,FlipkartScrapper.getShortUrl(url))
    # open("index.html","wb").write(scrapper.getHTML())
    # print(scrapper.url)
    # print(scrapper.getData())

    # url = "https://www.flipkart.com/sti-printed-men-round-neck-white-black-t-shirt/p/itm3b20cdb30cb02"
    # scrapper.updateUrl(FlipkartScrapper.getShortUrl(url))
    
    # print(scrapper.url)
    # print(scrapper.getData())