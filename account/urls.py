from . import views
from django.urls import path

app_name = 'account'

urlpatterns = [
    path('', views.CheckUsernameView.as_view(), name='check-username'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('verify/', views.VerifyCodeView.as_view(), name='verify-otp'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('forget/', views.ForgetView.as_view(), name='forget'),
    path('forget-verify/', views.ForgetOTPVerifyView.as_view(), name='forget-verify-otp'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),
    path('enter-otp/', views.EnterOTPView.as_view(), name='enter-otp'),
    path('enter-verify-otp/', views.EnterOTPVerifyView.as_view(), name='enter-verify-otp'),
    path('resend_otp/', views.ResendOTPView.as_view(), name='resend_otp'),
]