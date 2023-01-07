from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
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

