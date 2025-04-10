from django.urls import re_path, path
from . import views

app_name = 'product'

urlpatterns = [
    re_path(r'like/(?P<slug>[-\w]+)/', views.LikeView.as_view(), name='product_like'),
    re_path(r'^(?P<slug>[-\w]+)/$', views.ProductView.as_view(), name='product_detail'),
]