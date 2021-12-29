from django.shortcuts import render
from rest_framework.status import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from base.models import Auth, Key
from census.models import Census
from rest_framework.renderers import JSONRenderer
from authentication.serializers import UserSerializer
from administration.serializers import UserAdminSerializer, UserSerializer
from administration.serializers import *
from base.serializers import AuthSerializer, KeySerializer
from .serializers import CensusSerializer
from base.perms import IsAdminAPI
from utils.utils import get_ids, is_valid



def index(request):
    return render(request, "build/index.html")

class CensussAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request):
        query = Census.objects.all().values()
        return Response(query, status=HTTP_200_OK)

    def post(self, request):
        census = CensusSerializer(data=request.data)
        if not census.is_valid():
            return Response({"result", "Census object is not valid"}, status=HTTP_400_BAD_REQUEST)
        else:
            census.save()
            return Response({}, status=HTTP_200_OK)

    def delete(self, request):
        if request.data["idList"] is None:
            Census.objects.all().delete()
            return Response({}, status=HTTP_200_OK)
        else:
            ids = get_ids(request.data["idList"])
            Census.objects.filter(id__in=ids).delete()
            return Response({}, status=HTTP_200_OK)


class CensusAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request, census_id):
        try:
            query = Census.objects.all().values().filter(id=census_id).get()
        except ObjectDoesNotExist:
            return Response({}, status=HTTP_404_NOT_FOUND)
        return Response(query, status=HTTP_200_OK)

    def put(self, request, census_id):
        if not CensusSerializer(data=request.data).is_valid():
            return Response({"result": "Census object is not valid"}, status=HTTP_400_BAD_REQUEST)
        else:
            try:
                census= Census.objects.all().filter(id=census_id).get()
            except ObjectDoesNotExist:
                return Response({}, status=HTTP_404_NOT_FOUND)
            for key, value in request.data.items():
                setattr(census, key, value)
            census.save()
            return Response({}, status=HTTP_200_OK)

    def delete(self, request, census_id):
        Census.objects.all().filter(id=census_id).delete()
        return Response({}, status=HTTP_200_OK)

class CensussAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request):
        query = Census.objects.all().values()
        return Response(query, status=HTTP_200_OK)

    def post(self, request):
        census = CensusSerializer(data=request.data)
        if not census.is_valid():
            return Response({"result", "Census object is not valid"}, status=HTTP_400_BAD_REQUEST)
        else:
            census.save()
            return Response({}, status=HTTP_200_OK)

    def delete(self, request):
        if request.data.get("idList") is None:
            Census.objects.all().delete()
            return Response({}, status=HTTP_200_OK)
        else:
            ids = request.data.get("idList")
            Census.objects.filter(id__in=ids).delete()
            return Response({}, status=HTTP_200_OK)


class CensusAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request, census_id):
        try:
            query = Census.objects.all().values().filter(id=census_id).get()
        except ObjectDoesNotExist:
            return Response({}, status=HTTP_404_NOT_FOUND)
        return Response(query, status=HTTP_200_OK)

    def put(self, request, census_id):
        if not CensusSerializer(data=request.data).is_valid():
            return Response({"result": "Census object is not valid"}, status=HTTP_400_BAD_REQUEST)
        else:
            try:
                census = Census.objects.all().filter(id=census_id).get()
            except ObjectDoesNotExist:
                return Response({}, status=HTTP_404_NOT_FOUND)
            for key, value in request.data.items():
                setattr(census, key, value)
            census.save()
            return Response({}, status=HTTP_200_OK)

    def delete(self, request, census_id):
        Census.objects.all().filter(id=census_id).delete()
        return Response({}, status=HTTP_200_OK)


class AuthsAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request):
        query = Auth.objects.all().values()
        return Response(query, status=HTTP_200_OK)

    def post(self, request):
        auth = AuthSerializer(data=request.data)
        if not auth.is_valid():
            return Response({"result", "Auth object is not valid"}, status=HTTP_400_BAD_REQUEST)
        else:
            auth.save()
            return Response({}, status=HTTP_200_OK)

    def delete(self, request):
        if request.data.get("idList") is None:
            Auth.objects.all().delete()
            return Response({}, status=HTTP_200_OK)
        else:
            ids = request.data.get("idList")
            is_valid(len(ids) > 0, 'The ids list can not be empty')
            Auth.objects.filter(id__in=ids).delete()
            return Response({}, status=HTTP_200_OK)


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
            return Response({"result", "Key object is not valid"}, status=HTTP_400_BAD_REQUEST)
        else:
            key.save()
            return Response({}, status=HTTP_200_OK)

    def delete(self, request):
        if request.data.get("idList") is None:
            Key.objects.all().delete()
            return Response({}, status=HTTP_200_OK)
        else:
            ids = request.data.get("idList")
            is_valid(len(ids) > 0, 'The ids list can not be empty')
            Key.objects.filter(id__in=ids).delete()
            return Response({}, status=HTTP_200_OK)


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
        rest = UserAdminSerializer(query, many=True).data
        return Response(rest, status=HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        is_valid(serializer.is_valid(), "User object is not valid")
        fields = request.data
        user = User(username=fields['username'], first_name=fields['first_name'],
                    last_name=fields['last_name'], email=fields['email'], is_staff=False)
        user.set_password(request.data['password'])
        user.save()
        return Response({}, status=HTTP_200_OK)

    def delete(self, request):
        if request.data.get("idList") is None:
            User.objects.all().filter(is_superuser=False).delete()
            return Response({}, status=HTTP_200_OK)
        else:
            ids = request.data.get("idList")
            is_valid(len(ids) > 0, 'The ids list can not be empty')
            User.objects.filter(id__in=ids).delete()
            return Response({}, status=HTTP_200_OK)


class UserAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request, user_id):
        try:
            query = User.objects.filter(id=user_id).get()
        except ObjectDoesNotExist:
            return Response({}, status=HTTP_404_NOT_FOUND)
        rest = UserAdminSerializer(query).data
        return Response(rest, status=HTTP_200_OK)

    def put(self, request, user_id):
        user_update = UserUpdateSerializer(data=request.data)
        is_valid(user_update.is_valid(), "User object is not valid")
        try:
            user = User.objects.filter(id=user_id).get()
        except ObjectDoesNotExist:
            return Response({}, status=HTTP_404_NOT_FOUND)
        for key, value in request.data.items():
            if value:
                setattr(user, key, value)
        if request.data.get('password'):
            user.set_password(request.data['password'])
        user.save()
        return Response({}, status=HTTP_200_OK)

    def delete(self, request, user_id):
        User.objects.all().filter(is_superuser=False, id=user_id).delete()
        return Response({}, status=HTTP_200_OK)


class LoginAuthAPI(APIView):
    parser_classes = (parsers.FormParser,
                      parsers.MultiPartParser, parsers.JSONParser,)
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


class UpdateUserStateAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def post(self, request):
        ids = request.data.get("idList")
        state = request.data['state']
        value = request.data['value']
        is_valid(len(ids) > 0, 'The ids list can not be empty')
        is_valid(value == 'True' or value == 'False', 'The field value must be True or False')
        res = Response({}, status=HTTP_200_OK)
        if state == 'Active':
            users = User.objects.filter(id__in=ids)
            users.update(is_active=value)
        elif state == 'Staff':
            users = User.objects.filter(id__in=ids)
            users.update(is_staff=value)
        elif state == 'Superuser':
            users = User.objects.filter(id__in=ids)
            users.update(is_superuser=value)
        else:
            res = Response({"result": "The field state must be Active, Staff or Superuser"},
                           status=HTTP_400_BAD_REQUEST)
        return res
