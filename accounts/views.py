from django.contrib.auth import authenticate
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from accounts.serializers import AccountSerializer, SignUpSerializer


class SignUpView(APIView):
    permission_classes = []

    def post(self, request: HttpRequest) -> JsonResponse:
        serializer = SignUpSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return JsonResponse(status=status.HTTP_201_CREATED, data={"msg": "Sign Up Successful. User Created."})


class LoginView(APIView):
    permission_classes = []

    def post(self, request: HttpRequest) -> JsonResponse:
        serializer = AccountSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if not user:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST, data={"msg": "Invalid credentials."})

        token, _ = Token.objects.get_or_create(user=user)
        data = {
            "msg": "Login Successful.",
            "token": token.key
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)
