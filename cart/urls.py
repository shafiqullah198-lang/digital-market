from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('panel/', views.cart_panel, name='cart_panel'),
    # AJAX cart actions
    path('add/<int:product_id>/', views.cart_add_ajax, name='cart_add_ajax'),
    path('update/<int:item_id>/', views.cart_update_ajax, name='cart_update_ajax'),
    path('remove/<int:item_id>/', views.cart_remove_ajax, name='cart_remove_ajax'),
]

