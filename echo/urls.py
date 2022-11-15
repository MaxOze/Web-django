from django.urls import path
from .views import *

urlpatterns = [
    path('', start),
    path('shop/', shop, name='shop'),
    path('create/', create, name='create'),
    path('edit/<int:id>/', edit, name='edit'),
    path('delete/<int:id>/', delete, name='delete'),
    path('signup/', signUp, name='signup'),
    path('signin/', signIn, name='signin'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('tocart/<int:id>', toCart, name='tocart'),
    path('cart/', cart, name='cart'),
    path('orders/', orders, name='orders'),
    path('check/', checkLogin, name='check'),
    path('sort/', sort, name='sort'),
]