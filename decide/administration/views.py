from django.shortcuts import render
from base import serializers
from base.mods import query
from rest_framework.status import *
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from base.models import Auth, Key
from rest_framework.renderers import JSONRenderer

from authentication.serializers import UserSerializer
from base.serializers import AuthSerializer, KeySerializer
from base.perms import IsAdminAPI

import json


def index(request):
    return render(request, "build/index.html")

class AuthsAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request):
        query = Auth.objects.all().values()
        return Response(query, status=HTTP_200_OK)
    
    def post(self, request):
        auth = AuthSerializer(data=request.data)
        if not auth.is_valid():
            return Response({"result","Auth object is not valid"}, status=HTTP_400_BAD_REQUEST)
        else:
            auth.save()
            return Response({}, status=HTTP_200_OK)
    
    def delete(self, request):
        Auth.objects.all().delete()
        return Response({},status=HTTP_200_OK)
    
class AuthAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request, auth_id):
        try:
            query = Auth.objects.all().values().filter(id=auth_id).get()
        except ObjectDoesNotExist:
            return Response({}, status=HTTP_404_NOT_FOUND)
        return Response(query, status=HTTP_200_OK)

    def put(self, request, auth_id):
        if not AuthSerializer(data=request.data).is_valid():
            return Response({"result": "Auth object is not valid"}, status=HTTP_400_BAD_REQUEST)
        else:
            try:
                auth = Auth.objects.all().filter(id=auth_id).get()
            except ObjectDoesNotExist:
                return Response({}, status=HTTP_404_NOT_FOUND)
            for key, value in request.data.items():
                setattr(auth, key, value)
            auth.save()
            return Response({}, status=HTTP_200_OK)

    def delete(self, request, auth_id):
        Auth.objects.all().filter(id=auth_id).delete()
        return Response({}, status=HTTP_200_OK)

class KeysAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request):
        query = Key.objects.all().values()
        return Response(query, status=HTTP_200_OK)
    
    def post(self, request):
        key = KeySerializer(data=request.data)
        if not key.is_valid():
            return Response({"result","Key object is not valid"}, status=HTTP_400_BAD_REQUEST)
        else:
            key.save()
            return Response({}, status=HTTP_200_OK)
    
    def delete(self, request):
        Key.objects.all().delete()
        return Response({},status=HTTP_200_OK)

class KeyAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request, key_id):
        try:
            query = Key.objects.all().values().filter(id=key_id).get()
        except ObjectDoesNotExist:
            return Response({}, status=HTTP_404_NOT_FOUND)
        return Response(query, status=HTTP_200_OK)

    def put(self, request, key_id):
        if not KeySerializer(data=request.data).is_valid():
            return Response({"result": "User object is not valid"}, status=HTTP_400_BAD_REQUEST)
        else:
            try:
                keym = Key.objects.all().filter(id=key_id).get()
            except ObjectDoesNotExist:
                return Response({}, status=HTTP_404_NOT_FOUND)
            for key, value in request.data.items():
                setattr(keym, key, value)
            keym.save()
            return Response({}, status=HTTP_200_OK)

    def delete(self, request, key_id):
        Key.objects.all().filter(id=key_id).delete()
        return Response({}, status=HTTP_200_OK)

class UsersAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request):
        query = User.objects.all()
        rest = UserSerializer(query, many=True).data
        return Response(rest, status=HTTP_200_OK)

    def post(self, request):
        user = UserSerializer(data=request.data)
        if not user.is_valid():
            return Response({"result": "User object is not valid"}, status=HTTP_400_BAD_REQUEST)
        else:
            user.save()
            return Response({}, status=HTTP_200_OK)

    def delete(self, request):
        User.objects.all().filter(is_superuser=False).delete()
        return Response({}, status=HTTP_200_OK)


class UserAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request, user_id):
        try:
            query = User.objects.filter(id=user_id).get()
        except ObjectDoesNotExist:
            return Response({}, status=HTTP_404_NOT_FOUND)
        rest = UserSerializer(query).data
        return Response(rest, status=HTTP_200_OK)

    def put(self, request, user_id):
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

    def delete(self, request, user_id):
        User.objects.all().filter(is_superuser=False, id=user_id).delete()
        return Response({}, status=HTTP_200_OK)


class LoginAuthAPI(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        response = Response({}, status=HTTP_200_OK)
        response.set_cookie('token', token.key)
        return response


class LogoutAuthAPI(APIView):

    def get(self, request):
        response = Response({}, status=HTTP_200_OK)
        response.delete_cookie('token')
        return response
