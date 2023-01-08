from django.urls import path
from . import views

urlpatterns = [
    path('customer/signup/', views.customer_signup),
    path('customer/login/', views.customer_login),
    path('librarian/login/', views.librarian_login),
    path('books/search/', views.search_book),
    path('books/<int:book_pk>/borrow/', views.borrow_book),
    path('books/return/', views.return_book),
]

