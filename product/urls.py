from django.urls import re_path
from . import views

app_name = 'product'

urlpatterns = [
    re_path(r'(?P<slug>[-\w]+)/', views.ProductView.as_view(), name='product_detail'),
]