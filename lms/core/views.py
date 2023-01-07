from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, \
        authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from .models import *
from .forms import *
from .serializers import *

@api_view(['POST'])
def customer_signup(req: Request) -> Response:
    signup_form = SignupForm(req.data)
    if signup_form.is_valid():
        new_user = signup_form.save()
        new_customer = Customer.objects.create(user=new_user)
        new_customer.save()
        token = Token.objects.create(user=new_user)
        return Response(f'Token {token.key}', status.HTTP_201_CREATED)

    return Response(f'{signup_form.error_messages}', status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['POST'])
def customer_login(req: Request) -> Response:
    login_form = LoginForm(req, req.data)
    if login_form.is_valid():
        logged_user = login_form.get_user()

        try:
            Customer.objects.get(user=logged_user)
        except Customer.DoesNotExist:
            return Response('Librarians cannot login to Customer interface', status.HTTP_403_FORBIDDEN)

        token, _ = Token.objects.get_or_create(user=logged_user)
        return Response(f"Token {token.key}", status=status.HTTP_200_OK)

    return Response(f"{login_form.error_messages}", status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['POST'])
def librarian_login(req: Request) -> Response:
    login_form = LoginForm(req, req.data)
    if login_form.is_valid():
        logged_user = login_form.get_user()

        try:
            Librarian.objects.get(user=logged_user)
        except Librarian.DoesNotExist:
            return Response('ummm, what are you doing here?\nthis area is offlimits', status.HTTP_403_FORBIDDEN)

        token, _ = Token.objects.get_or_create(user=logged_user)
        return Response(f"Token {token.key}", status=status.HTTP_200_OK)

    return Response(f"{login_form.error_messages}", status=status.HTTP_406_NOT_ACCEPTABLE)

@api_view(['GET'])
def search_book(req: Request) -> Response:
    title = req.data.get('title') or ''
    authors = req.data.get('authors') or ''
    publisher = req.data.get('publisher') or ''
    genre = req.data.get('genre') or ''

    queryset = Book.objects.filter(
            title__contains=title,
            authors__contains=authors,
            publisher__contains=publisher,
            genres__contains=genre,
            )

    serializer = BookSerializer(queryset, many=True)

    return Response(serializer.data, status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def borrow_book(req: Request, book_pk: int) -> Response:
    book = get_object_or_404(Book, pk=book_pk)
    borrower = req.data.get('borrower') or ''
    # TODO: validate date of retrival
    date_of_retrival = req.data.get('date_of_retrival') or ''

    if not borrower:
        return Response("Customer Not Found", status=status.HTTP_400_BAD_REQUEST)

    if not date_of_retrival:
        return Response("Date of Retrival not Specified", status.HTTP_400_BAD_REQUEST)

    borrower = get_object_or_404(Customer, user__username=borrower)
    checker = req.user

    try:
        checker = Librarian.objects.get(user=req.user)
    except Librarian.DoesNotExist:
        return Response('Only Librarians can register borrowings', status.HTTP_403_FORBIDDEN)

    borrow_record = Borrow(
            borrower=borrower,
            checker=checker,
            date_of_retrival=date_of_retrival
            )
    borrow_record.save()
    borrow_record.book.add(book)
    borrow_record.save()

    return Response(status=status.HTTP_200_OK)
