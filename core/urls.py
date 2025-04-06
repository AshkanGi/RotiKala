from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('faq/', views.FaqView.as_view(), name='faq'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('whyus/', views.WhyUsView.as_view(), name='why'),
    path('howtoby/', views.HowToBuyView.as_view(), name='buy'),
]