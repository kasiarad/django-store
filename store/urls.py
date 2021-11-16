from django.urls import path
from . import views


urlpatterns=[
    path('', views.StoreView.as_view(), name="store"),
    path('cart/', views.CartView.as_view(), name="cart"),
    path('about/', views.About.as_view(), name="about"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
]
