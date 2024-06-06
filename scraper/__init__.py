from abc import ABC, abstractmethod 
from fake_useragent import UserAgent
from pathlib import Path
import os, random, requests, logging
from datetime import datetime 
from bs4 import BeautifulSoup
import base64, io, numpy as np
from PIL import Image

ua = UserAgent(platforms="pc")

log_dir=Path("logs/images/")
if not os.path.exists(log_dir): os.makedirs(log_dir)


apis = [
  "https://anuj-panthri-puppeteer-api-1.hf.space/screenshot/",
  "https://anuj-panthri-puppeteer-api-2.hf.space/screenshot/",
  "https://shivam-kala-puppeteer-api-3.hf.space/screenshot/",
  "https://shivam-kala-puppeteer-api-4.hf.space/screenshot/",
  ]

def getHTMLFROMAPI(url) -> tuple[str, str]:
    
    api = apis[random.randint(0,len(apis)-1)]

    headers = {
        "Accept-language": "en-GB,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "User-agent": ua.random
    }
    data = {
        "url":url,
        "headers":headers,
    }
    logging.info("using_api:",api)
    try:
        response = requests.post(api, data=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        res = response.json()
    except requests.RequestException as e:
        logging.error(f"Error while hitting puppeteer API for URL {url}: {e}")
        res = {"html": "", "base64": ""}  # Ensure res is defined
    except ValueError as e:  # In case response is not JSON
        logging.error(f"Error parsing JSON response for URL {url}: {e}")
        res = {"html": "", "base64": ""}

    return res["html"].encode("UTF-8"), res["base64"].encode("UTF-8")

class BaseScrapper(ABC):
    def __init__(self,url):
        self.updateUrl(url)

    def takeScreenshot(self):
        cur_time = datetime.now()
        img_path = log_dir/Path(f"{cur_time.day}-{cur_time.month}-{cur_time.year}--{cur_time.hour}-{cur_time.minute}-{cur_time.second}.png")
        bytes_array = io.BytesIO(base64.b64decode(self.base64))
        image = np.array(Image.open(bytes_array).convert("RGB"))
        Image.fromarray(image).save(img_path)
        
        

    @classmethod
    def getBaseUrl(cls,url):
        return "/".join(url.split("/",3)[:3])+"/"

    @classmethod
    def getShortUrl(cls,url):
        return url
    
    def updateUrl(self,url):
        self.url=url 
        # gethtml from api and make a temp html file out of it
        self.html,self.base64 = getHTMLFROMAPI(url)    
        self.soup = BeautifulSoup(self.html, "html.parser")

    def getHTML(self):
        return self.html

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
            # print(self)
            return f(*args,**kwargs)
        except Exception as e:
            print(e)

    return exec

class AmazonScrapper(BaseScrapper):
    def __init__(self,url):
        super().__init__(url)

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
        return self.soup.find("span",{"id":"productTitle"}).text.strip()
    
    @error_handler
    def getPrice(self):
        
        base_element = self.soup.find("div",{"id":"corePriceDisplay_desktop_feature_div"})
        if(base_element is None):
            base_element = self.soup.find("div",{"id":"corePrice_desktop"})

        base_element = base_element.find("div",{"class":"a-section"}).find("span",{"class":"a-price"})


        # removing unnecessary elements
        offscreen_element = base_element.find("span",{"class":"a-offscreen"})
        decimal_element = base_element.find("span",{"class":"a-price-decimal"})
        if (offscreen_element):    offscreen_element.extract()
        if (decimal_element):    decimal_element.extract()
        
        # print(base_element)

        try:
            symbol= base_element.find("span",{"class":"a-price-symbol"}).text
            whole = base_element.find("span",{"class":"a-price-whole"}).text
            decimal= '.'
            fraction = base_element.find("span",{"class":"a-price-fraction"}).text
            return symbol + whole + decimal + fraction
        except:
            return base_element.text
        
        
    @error_handler
    def getImage(self):
        return self.soup.find("img",{"id":"landingImage"}).get("src")
        
    def getData(self):
        data = {
            "title":self.getTitle(),
            "price":self.getPrice(),
            "image":self.getImage(),
        }

        if data["price"]==None or data["title"]==None or data["image"]==None :   self.takeScreenshot()
        return data

class FlipkartScrapper(BaseScrapper):
    def __init__(self,url):
        super().__init__(url)
    
    @classmethod
    def getShortUrl(cls,url):
        return url.split("?",1)[0]
    
    @error_handler
    def getTitle(self):
        return self.soup.find("span",{"class":"VU-ZEz"}).text.strip()
        
    @error_handler
    def getPrice(self):
        return self.soup.find("div",{"class":"hl05eU"}).find("div",{"class":"CxhGGd"}).text

    @error_handler
    def getImage(self):
        return self.soup.find("div",{"class":"_6lpKCl"}).find("img").get("src")
        
    def getData(self):
        data = {
            "title":self.getTitle(),
            "price":self.getPrice(),
            "image":self.getImage(),
        }

        if data["price"]==None or data["title"]==None or data["image"]==None :   self.takeScreenshot()
        return data

if __name__ == "__main__":
    # https://www.amazon.in/dp/B07WHQRN1B/
    # https://www.flipkart.com/p/itm3b20cdb30cb02
    # url = "https://www.amazon.in/dp/B07WHQRN1B/"
    html,base64_str = getHTMLFROMAPI("https://bot.sannysoft.com/")

    bytes_array = io.BytesIO(base64.b64decode(base64_str))
    image = np.array(Image.open(bytes_array).convert("RGB"))
    Image.fromarray(image).save("img_path.jpg")

    # url = "https://www.amazon.com/dp/B088SKYMF2/"
    url = "https://www.amazon.com/dp/B0CYCKS9S4?th=1"
    # url = "https://www.amazon.com/dp/B08F2/"
    # url = "https://wasdasdzx2/"

    
    # print(getHTMLFROMAPI(url))
    scrapper = AmazonScrapper(AmazonScrapper.getShortUrl(url))
    print(scrapper.url)
    data=scrapper.getData()
    print(data)
    # scrapper.takeScreenshot()
    # open("index.html","wb").write(scrapper.getHTML())
    # # input("stop")
    # exit()

    # url = "https://www.amazon.com/dp/B07PVCK9KX/"
    # scrapper.updateUrl(AmazonScrapper.getShortUrl(url))
    # print(scrapper.url)
    # print(scrapper.getData())
    
    # url = "https://www.amazon.com/dp/B07CNPBS7T/"
    # scrapper.updateUrl(AmazonScrapper.getShortUrl(url))
    # print(scrapper.url)
    # print(scrapper.getData())

    # # url = "https://www.amazon.com/Hope-Rainbow-Hoda-Kotb/dp/0593624122/?_encoding=UTF8&_encoding=UTF8&ref_=dlx_gate_sd_dcl_tlt_fa13649f_dt_pd_gw_unk&pd_rd_w=FPLOl&content-id=amzn1.sym.81a68cec-8afc-4296-99f7-78cf5ddc15b5&pf_rd_p=81a68cec-8afc-4296-99f7-78cf5ddc15b5&pf_rd_r=KAD1QPN234SH5MXYBNW6&pd_rd_wg=A7ZKi&pd_rd_r=fa39bbc3-93b1-41a2-b592-77d89dfc6566"
    # # url = "https://www.amazon.in/Lux-Cozi-Melange-Regular-Sleeves/dp/B0CH9QMFF4/ref=sl_ob_desktop_dp_0_2_v2?_encoding=UTF8&pd_rd_w=1Bm0J&content-id=amzn1.sym.cdbcd11c-3329-43cb-9547-fb297b2c655b&pf_rd_p=cdbcd11c-3329-43cb-9547-fb297b2c655b&pf_rd_r=PTKWAM93FTVZKNGQFPVM&pd_rd_wg=iE7ky&pd_rd_r=ccfc3bd0-e267-435c-85d3-f63c78a1db0a"
    # url = "https://www.amazon.in/dp/B0CHM745CT/ref=syn_sd_onsite_desktop_0?ie=UTF8&pd_rd_plhdr=t&aref=94rDEQyVIg&th=1"
    # scrapper.updateUrl(AmazonScrapper.getShortUrl(url))
    # print(scrapper.url)
    # print(scrapper.getData())
    url = "https://www.flipkart.com/play-mp1-a-smart-wifi-3d-4k-full-hd-led-recently-launched-android-8-0-projector-genuine-multifunction-home-office-entertainment-bluetooth-4d-keystone-300-inch-display-1920x1080p-portable-mini-digital-projector-vga-usb-hdmi-home-theater-5500-lm-wireless-remote-controller-projector/p/itm074a5ffecaaeb?pid=PROG8669KWF79N4M&lid=LSTPROG8669KWF79N4M5BASUJ&marketplace=FLIPKART&store=6bo%2Ftia%2F1hx&srno=b_1_1&otracker=browse&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_4_L2_view-all&fm=organic&iid=en_LBb1tb_UvM8GDd2JetuL0M6u7M3PThc2nRcqXv_7SjYSgFAwhjvAn5iFH5HT8M7N9ND-3dLak-GrZ3KhUbsG3g%3D%3D&ppt=browse&ppn=browse&ssid=ve9vmvg0dc0000001713290617288"
    url = 'https://www.flipkart.com/apple-iphone-15-blue-128-gb/p/itmbf14ef54f645d?pid=MOBGTAGPAQNVFZZY&lid=LSTMOBGTAGPAQNVFZZYO7HQ2L&marketplace=FLIPKART&store=tyy%2F4io&spotlightTagId=BestsellerId_tyy%2F4io&srno=b_1_1&otracker=browse&fm=organic&iid=fedd7fea-5ff7-4bd7-a5f0-a9008f1702c3.MOBGTAGPAQNVFZZY.SEARCH&ppt=browse&ppn=browse&ssid=7un6hxsq6o0000001710258321538'
    scrapper = FlipkartScrapper(FlipkartScrapper.getShortUrl(url))
    # open("index.html","wb").write(scrapper.getHTML())
    print(scrapper.url)
    print(scrapper.getData())

    # url = "https://www.flipkart.com/sti-printed-men-round-neck-white-black-t-shirt/p/itm3b20cdb30cb02"
    # scrapper.updateUrl(FlipkartScrapper.getShortUrl(url))
    
    # print(scrapper.url)
    # print(scrapper.getData())