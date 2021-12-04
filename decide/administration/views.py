from django.shortcuts import render
from rest_framework.status import *
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.serializers import UserSerializer
from base.perms import IsAdminAPI


def index(request):
    return render(request, "build/index.html")


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
