from django.urls import path
from .views import (
    BaseView,
    ProductDetailView,
    CartView,
    AddToCartView,
    DeleteFromCartView,
    register

)
from django.urls.conf import include
import django.contrib.auth.urls as auth_urls


urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(),
         name='product_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(),
         name='add_to_cart'),
    path('del-from-cart/<str:ct_model>/<str:slug>/',
         DeleteFromCartView.as_view(), name='del_from_cart'),
    path('accounts/', include(auth_urls)),
    path('register/', register, name='register'),
]
