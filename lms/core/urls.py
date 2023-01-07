from django.urls import path
from . import views

urlpatterns = [
    path('customer/signup/', views.customer_signup),
    path('customer/login/', views.customer_login),
]

