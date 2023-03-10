from django.db import models
from django.contrib.auth import models as authmodels

class Customer(models.Model):
    user = models.OneToOneField(authmodels.User, on_delete=models.CASCADE)
    allowed_to_borrow = models.BooleanField(default=True)

class Librarian(models.Model):
    user = models.OneToOneField(authmodels.User, on_delete=models.CASCADE)
    salary = models.FloatField(default=1200.0)

# this function is to be use by an admin to add librarians
def create_librarian(username: str, password: str) -> Librarian:
    user = authmodels.User(username=username)
    user.set_password(password)
    user.save()

    librarian = Librarian(user=user)
    librarian.save()
    
    return librarian

class Book(models.Model):
    title = models.CharField(max_length=250)
    authors = models.CharField(max_length=600)
    publisher = models.CharField(max_length=100)
    publishing_date = models.DateTimeField()
    genres = models.CharField(max_length=100)
    count = models.IntegerField(blank=False, null=False, default=0)
    available = models.BooleanField(default=True)

class Wishlist(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    list_of_books = models.ManyToManyField(Book, 'favored_book')
    is_public = models.BooleanField(default=False)

class Borrow(models.Model):
    borrower = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='borrower')
    # TODO: use something more appropriate that CASCADE
    checker = models.ForeignKey(Librarian, on_delete=models.CASCADE, related_name='checker')
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    date_of_borrowing = models.DateTimeField(auto_now=True)
    date_of_retrival = models.DateTimeField()

