from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('user/', include('account.urls')),
    path('user_profile/', include('user_profile.urls')),
    path('product/', include('product.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('checkout/', include('cart.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
