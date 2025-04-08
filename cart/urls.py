from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('cart', views.CartDetail.as_view(), name='cart_detail'),
    path('add/<int:pk>', views.CartAdd.as_view(), name='add_product'),
    path('remove/<str:id>', views.CartRemove.as_view(), name='remove_product'),
    path('cart_clear', views.CartClear.as_view(), name='cart_clear'),
    path('shipping', views.CartShipping.as_view(), name='cart_shipping'),
    path('payment/<int:pk>', views.CartPayment.as_view(), name='cart_payment'),
    path('order_creat', views.OrderCreation.as_view(), name='order_creat'),
    path('discount/<int:pk>', views.ApplyDiscount.as_view(), name='discount'),
]