from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from scraper.scraper import *
from .models import Product,Price,Track
import json
# from . import scheduled_jobs

def getScrapper(url):
    if("amazon" in url.lower()):
        return AmazonScrapper(url)
    elif("flipkart" in url.lower()):
        return FlipkartScrapper(url)
    else:
        return None


# Create your views here.
def home(request):
    # return render(request,"main/index.html",context={})
    return redirect("/accounts/google/login")


@login_required(login_url="/")
def add_product(request):
    
    if(request.method=="GET"):
        return render(request,"main/main_screen.html",context={})

    elif(request.method=="POST"):
        print(request.POST)

        old_prod = Product.objects.filter(url=request.POST["url"])
        if (len(old_prod)>0):
            return render(request,"main/main_screen.html",context={"error":"already tracking this url"})
        
        try:
            scrapper = getScrapper(request.POST["url"])
        except:
            return render(request,"main/main_screen.html",context={"error":"invalid url"})
    
        if(scrapper==None):
            return render(request,"main/main_screen.html",context={"error":"unsupported url"})

            
        data = scrapper.getData()
        print(data)
        # html = str(scrapper.soup.prettify())
        # # print(html)
        # res = {"html": html}
        # json_data = json.dumps(res)
        # return HttpResponse(json_data, content_type = "application/json")
        if(data["title"]==None):
            print("title error")
            # return HttpResponse(scrapper.soup)
            return render(request,"main/main_screen.html",context={"error":"Failed to fetch data"})
        if(data["price"]==None):
            print("price error")
            # return HttpResponse(scrapper.soup)
            # return HttpResponse(json.dumps({"html": scrapper.soup}))
            return render(request,"main/main_screen.html",context={"error":"Failed to fetch data"})
        if(data["image"]==None):
            print("image error")
            # return HttpResponse(scrapper.soup)
            # return HttpResponse(json.dumps({"html": scrapper.soup}))
            return render(request,"main/main_screen.html",context={"error":"Failed to fetch data"})

        # document.querySelector("span.a-price span");
        print("price:",data["price"])
        if(data["price"].strip(" ")==""):
            return HttpResponse(scrapper.soup)
        # save product
        # print(request.user)
        product = Product(
            url=request.POST["url"],
            title=data["title"],
            image=data["image"]
            )
        
        product.save()

        # save track
        track = Track(user=request.user,product=product)
        track.save()
        
        # save price
        price = Price(
            product=product,
            price=data['price']
        )
        price.save()

        return redirect(reverse("detail",kwargs={"id":product.id}))

@login_required(login_url="/")
def product_detail(request,id):
    product = get_object_or_404(Product,id=id)
    return render(request,"main/product_detail_screen.html",context={"product":product})

@login_required(login_url="/")
def all_products(request):
    tracks = Track.objects.filter(user=request.user) 
    products = [track.product for track in tracks]
    
    return render(request,"main/all_products.html",context={"products":products})


@login_required(login_url="/")
def delete_product(request,id):
    if request.method=="POST":
        track = get_object_or_404(Track,product__id=id)
        track.delete() 

        return HttpResponse(status=204)


