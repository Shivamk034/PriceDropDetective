from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from scraper.scraper import *
from .models import Product,Price

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

        try:
            scrapper = getScrapper(request.POST["url"])
        except:
            return render(request,"main/main_screen.html",context={"error":"invalid url"})
    
        if(scrapper==None):
            return render(request,"main/main_screen.html",context={"error":"unsupported url"})

            
        data = scrapper.getData()

        if(data["title"]==None):
            return render(request,"main/main_screen.html",context={"error":"Failed to fetch data"})
        if(data["price"]==None):
            return render(request,"main/main_screen.html",context={"error":"Failed to fetch data"})
        if(data["image"]==None):
            return render(request,"main/main_screen.html",context={"error":"Failed to fetch data"})

        # save product
        # print(request.user)
        product = Product(
            user=request.user,
            url=request.POST["url"],
            title=data["title"],
            image=data["image"]
            )
        
        product.save()

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
    products = Product.objects.filter(user=request.user)
    
    return render(request,"main/all_products.html",context={"products":products})
