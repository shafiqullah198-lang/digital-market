from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home
from products.views import sell_buy, sell



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),

    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('sell-buy/', sell_buy, name='sell_buy'),
    path('sell/', sell, name='sell'),
    path('', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
