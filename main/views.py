from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from scraper import *
from .models import Product,Price,Track
import os
from PIL import Image

def getScrapper(url):
    if("amazon" in url.lower()):
        return AmazonScrapper
    elif("flipkart" in url.lower()):
        return FlipkartScrapper
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
        # check if url is supported
        scrapperClass = getScrapper(request.POST["url"])
        
        if(scrapperClass==None):
            # EXPERIMENT !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # scrapper = AmazonScrapper(request.POST["url"])
            # scrapper.getData()
            return render(request,"main/main_screen.html",context={"error":"unsupported url"})
        
        try:
            url = scrapperClass.getShortUrl(request.POST["url"])
            print("url:",url)
        except:
            # if we were unable to get the short url
            return render(request,"main/main_screen.html",context={"error":"invalid url"})
            
        # check if already tracking
        track = Track.objects.filter(user=request.user,product__url=url)
        if(len(track)>0):
            return render(request,"main/main_screen.html",context={"error":"already tracking this url"})

        # handling when driver is unable to get the page (the url might be wrong)
        try:
            scrapper = scrapperClass(url)
        except Exception as e:
            print(e)
            return render(request,"main/main_screen.html",context={"error":"invalid url"})
        
        # check if product is already tracked by someone
        old_prod = Product.objects.filter(url=url)
        if (len(old_prod)>0):
            track = Track(user=request.user,product=old_prod[0])
            track.save()
            return redirect(reverse("detail",kwargs={"id":old_prod[0].id}))
    
        data = scrapper.getData()

        if(data["title"]==None):
            print("title error")
            return render(request,"main/main_screen.html",context={"error":"Failed to fetch data"})
        if(data["price"]==None):
            print("price error")
            return render(request,"main/main_screen.html",context={"error":"Failed to fetch data"})
        if(data["image"]==None):
            print("image error")
            return render(request,"main/main_screen.html",context={"error":"Failed to fetch data"})
    
        if not Price.isValidPrice(data['price']):  
            return render(request,"main/main_screen.html",context={"error":"something went wrong"})
        
        # save product
        product = Product(
            url=url,
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
        track = get_object_or_404(Track,user=request.user,product__id=id)
        track.delete() 

        return HttpResponse(status=204)

@login_required(login_url="/")
def get_image(request,path):
    if(not request.user.is_superuser):
       HttpResponse(status=401)
    
    base_image = Image.open("logs/images/"+path)
    
    response = HttpResponse(content_type="image/png")
    base_image.save(response,"PNG")
    return response

@login_required(login_url="/")
def logs_view(request):
    if(not request.user.is_superuser):
       HttpResponse(status=401)
    
    # get all the logs screenshots in latest to oldest order
    # print(Path("logs/images/*.png"))
    image_list = os.listdir("logs/images/")
    image_list.sort(reverse=True)
    return render(request,"main/logs.html",context={"image_list":image_list})