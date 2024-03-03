from django.urls import path
from . import views
urlpatterns = [
    path("",views.home,name='login'),
    path("add/",views.add_product,name='add'),
    path("detail/<id>",views.product_detail,name='detail'),
]