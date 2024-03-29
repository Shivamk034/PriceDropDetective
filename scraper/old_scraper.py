import requests
from bs4 import BeautifulSoup
from flask import Flask

# url = "https://www.amazon.com/dp/B09VBZM2L6/"
urls =[
    # "https://www.amazon.in/",
    # "https://www.amazon.in/s?k=westwood+guitar&crid=ABDMBK1FQSD6&sprefix=westwood+%2Caps%2C379&ref=nb_sb_ss_ts-doa-p_1_9",
    # "https://www.amazon.in/dp/B0B9YK24TF/",
    # "https://www.amazon.in/dp/B09G9FPGTN/",
    # "https://www.amazon.in/dp/B09V44MF6K",
    # "https://www.amazon.in/dp/B0BXNYVRYX/",
    # "https://www.amazon.in/dp/B0CKR1SS34/",
    "https://www.amazon.in/dp/B0CMDBBKSX/",
]

headers = {
        # "Accept-language": "en-GB,en;q=0.9",
        # "Accept-Encoding": "gzip, deflate, br",
        # "Cache-Control": "max-age=0",
        # "Connection": "keep-alive",
        # "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    }

data = {
    "url":urls[0],
    "headers":headers,
}


app = Flask(__name__)

def getData(url,headers={}):
  html = requests.post("https://anuj-panthri-puppeteer-api.hf.space/html/",data={"url":url,"headers":headers}).json()["html"]
  return html



@app.route("/",methods=["GET"])
def home():
  for url in urls:
    print("Started")
    html = getData(url,headers)
    print("Ended")
  return html


# html = getData(url)
# soup = BeautifulSoup(html, 'html.parser')
# img = soup.find_all("img")
# print(html)

app.run(debug=True)