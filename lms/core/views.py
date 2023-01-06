from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .models import *
from .forms import *

__all__ = ['customer_signup']

@api_view(['POST'])
def customer_signup(req: Request) -> Response:
    signup_form = CustomerSignupForm(req.data)
    if signup_form.is_valid():
        new_user = signup_form.save()
        token = Token.objects.create(user=new_user)
        return Response(f'Token {token.key}', status.HTTP_201_CREATED)

    return Response(f'{signup_form.error_messages}', status=status.HTTP_406_NOT_ACCEPTABLE)


