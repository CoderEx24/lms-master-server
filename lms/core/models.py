from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=250)
    authors = models.CharField(max_length=600)
    publisher = models.CharField(max_length=100)
    publishing_date = models.DateTimeField()
    genres = models.CharField(max_length=100)
    count = models.IntegerField(blank=False, null=False, default=0)

class Wishlist(models.Model):
    user = models.ForeignKey(User)
    list_of_books = models.ManyToManyField(Book, 'favored_book')
    is_public = models.BooleanField(default=False)

class Borrow(models.Model):
    borrower = models.ForeignKey(User)
    book = models.ManyToManyField(Book, related_name='borrowed_book')
    date_of_borrowing = models.DateTimeField(auto_now=True)
    date_of_retrival = models.DateTimeField()

