# lms-master-server
This repository contains the master server.
The master server will handle authentication and database management.

## Structure
The database will contain the following tables:-

- Book
    This will contain all the information about books.
    Fields:-
    - title
    - authors
    - publisher
    - publishing date
    - genres
    - count

- Wishlist 
    This will contain a list of books the a user can choose.
    Users can choose to share their wishlists or not.
    Fields:-
    - user (as foreign key)
    - list-of-books
    - is-public

- Borrow
    This will contain the information related to book borrowing.
    A record is added each time a user borrows a book.

    On successful borrowing, the `count` field on the borrowed book must be decremented.
    Fields:-
    - borrower (as a foreign key)
    - book (as a foreign key)
    - date of borrowing
    - date of retrival

Django's user model (`django.contrib.auth.models.User`) 
will be used for the users and library admins.

## API Endpoints
The master server will expose the following endpoints.
All endpoints require an API key to function.

- `/customer/login`
    takes authentication information as input (username, **hashed** password).
    returns an auth token on successful authentication and an error code otherwise.

- `/customer/register`
    Resgisters a new customer.
    In addition to an API key, an authenticated library admin is required
    for the success of this operation.
    returns a success code on successful registeration, and an error code otherwise.

