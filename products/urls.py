from django.urls import path
from . import views
from .views import proceed
from .views import checkout_success
from .views import easypaisa_payment
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('sell/',views.sell, name='sell'),
    path('proceed/', proceed, name='proceed'),  
    path('checkout/success/', checkout_success, name='checkout_success'),
    path('products/payment/', easypaisa_payment, name='payment'),
    path("download/<int:pk>/", views.download_project, name="download_project"),
    





]

