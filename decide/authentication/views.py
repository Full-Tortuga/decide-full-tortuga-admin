import rest_framework.status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from .serializers import UserSerializer


class GetUserView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        return Response(UserSerializer(tk.user, many=False).data)


class LogoutView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        try:
            tk = Token.objects.get(key=key)
            tk.delete()
        except ObjectDoesNotExist:
            pass

        return Response({})


class RegisterView(APIView):
    def post(self, request):
        key = request.data.get('token', '')
        tk = get_object_or_404(Token, key=key)
        if not tk.user.is_superuser:
            return Response({}, status=HTTP_401_UNAUTHORIZED)

        username = request.data.get('username', '')
        pwd = request.data.get('password', '')
        if not username or not pwd:
            return Response({}, status=HTTP_400_BAD_REQUEST)

        try:
            user = User(username=username)
            user.set_password(pwd)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
        except IntegrityError:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        return Response({'user_pk': user.pk, 'token': token.key}, HTTP_201_CREATED)


class UsersAPI(APIView):
    def get(self, request):
        key = request.META.get("HTTP_TOKEN", "")
        try:
            tk = get_object_or_404(Token, key=key)
        except Http404:
            return Response({"Error": "Invalid token"}, status=HTTP_401_UNAUTHORIZED)
        if tk.user.is_superuser is True:
            query = User.objects.all()
            rest = UserSerializer(query, many=True).data
            return Response(rest, status=HTTP_200_OK)

    def post(self, request):
        key = request.META.get("HTTP_TOKEN", "")
        try:
            tk = get_object_or_404(Token, key=key)
        except Http404:
            return Response({"Error": "Invalid token"}, status=HTTP_401_UNAUTHORIZED)

        if tk.user.is_superuser is True:
            user = UserSerializer(data=request.data)
            if not user.is_valid():
                return Response({"result": "User object is not valid"}, status=HTTP_400_BAD_REQUEST)
            else:
                user.save()
                return Response({}, status=HTTP_200_OK)
        else:
            return Response({"Error": "You are not authenticated to perform this request"},
                            status=HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        key = request.META.get("HTTP_TOKEN", "")
        try:
            tk = get_object_or_404(Token, key=key)
        except Http404:
            return Response({"Error": "Invalid token"}, status=HTTP_401_UNAUTHORIZED)
        if tk.user.is_superuser is True:
            query = User.objects.all().filter(is_superuser=False).delete()
            return Response({}, status=HTTP_200_OK)


class UserAPI(APIView):
    def get(self, request, user_id):
        key = request.META.get("HTTP_TOKEN", "")
        try:
            tk = get_object_or_404(Token, key=key)
        except Http404:
            return Response({"Error": "Invalid token"}, status=HTTP_401_UNAUTHORIZED)

        if tk.user.is_superuser is True:
            try:
                query = User.objects.filter(id=user_id).get()
            except ObjectDoesNotExist:
                return Response({}, status=HTTP_404_NOT_FOUND)
            rest = UserSerializer(query).data
            return Response(rest, status=HTTP_200_OK)
        else:
            return Response({"Error": "You are not authenticated to perform this request"},
                            status=HTTP_401_UNAUTHORIZED)

    def put(self, request, user_id):
        key = request.META.get("HTTP_TOKEN", "")
        try:
            tk = get_object_or_404(Token, key=key)
        except Http404:
            return Response({"Error": "Invalid token"}, status=HTTP_401_UNAUTHORIZED)

        if tk.user.is_superuser is True:
            if not UserSerializer(data=request.data).is_valid():
                return Response({"result": "User object is not valid"}, status=HTTP_400_BAD_REQUEST)
            else:
                try:
                    user = User.objects.filter(id=user_id).get()
                except ObjectDoesNotExist:
                    return Response({}, status=HTTP_404_NOT_FOUND)
                for key, value in request.data.items():
                    setattr(user, key, value)
                user.save()
                return Response({}, status=HTTP_200_OK)
        else:
            return Response({"Error": "You are not authenticated to perform this request"},
                            status=HTTP_401_UNAUTHORIZED)

    def delete(self, request, user_id):
        key = request.META.get("HTTP_TOKEN", "")
        try:
            tk = get_object_or_404(Token, key=key)
        except Http404:
            return Response({"Error": "Invalid token"}, status=HTTP_401_UNAUTHORIZED)
        if tk.user.is_superuser is True:
            query = User.objects.all().filter(is_superuser=False, id=user_id).delete()
            return Response({}, status=HTTP_200_OK)
        else:
            return Response({"Error": "You are not authenticated to perform this request"},
                            status=HTTP_401_UNAUTHORIZED)
