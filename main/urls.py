from django.urls import path
from . import views
urlpatterns = [
    path("",views.home,name='login'),
    path("add/",views.add_product,name='add'),
    path("detail/<id>",views.product_detail,name='detail'),
    path("all_products/",views.all_products,name='all_products'),
    path("delete/<id>",views.delete_product,name="delete_product"),
]