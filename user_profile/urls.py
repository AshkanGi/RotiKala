from django.urls import path
from . import views

app_name = 'user_profile'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('orders/', views.OrdersView.as_view(), name='orders'),
    path('favorites/', views.FavoritesView.as_view(), name='favorites'),
    path('recent/', views.RecentView.as_view(), name='recent'),
    path('notification/', views.NotificationView.as_view(), name='notification'),
    path('address/', views.AddressView.as_view(), name='address'),
    path('edit/', views.EditView.as_view(), name='edit'),
]