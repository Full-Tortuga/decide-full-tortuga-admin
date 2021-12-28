from django.shortcuts import render
from rest_framework.status import *
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from base.models import Auth, Key

from administration.serializers import UserAdminSerializer, UserSerializer, AdminQuestionSerializer
from base.serializers import AuthSerializer, KeySerializer
from base.perms import IsAdminAPI
from utils.utils import get_ids, is_valid
from voting.models import Question



def index(request):
    return render(request, "build/index.html")

class QuestionsAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request):
        query = Question.objects.all()
        rest = AdminQuestionSerializer(query, many=True).data
        return Response(rest, status=HTTP_200_OK)

    def post(self, request):
        question = AdminQuestionSerializer(data=request.data)
        if not question.is_valid():
            return Response({"result","AdminQuestion object is not valid"}, status=HTTP_400_BAD_REQUEST)
        else:
            question.save()
            return Response({}, status=HTTP_200_OK)

    def delete(self, request):
        if request.data["idList"] is None:
            Question.objects.all().delete()
            return Response({}, status=HTTP_200_OK)
        else:
            ids = get_ids(request.data["idList"])
            is_valid(len(ids) > 0, 'The format of the ids list is not correct')
            Question.objects.filter(id__in=ids).delete()
            return Response({}, status=HTTP_200_OK)

class QuestionAPI(APIView):
    permission_classes = (IsAdminAPI,)

    def get(self, request, question_id):
        try:
            query = Question.objects.filter(id=question_id).get()
        except ObjectDoesNotExist:
            return Response({}, status=HTTP_404_NOT_FOUND)
        rest = AdminQuestionSerializer(query).data
        return Response(rest, status=HTTP_200_OK)

    def put(self,request,question_id):
       obj = Question.objects.get(id=question_id)
       serializer = AdminQuestionSerializer(obj,data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=HTTP_200_OK)
       return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, question_id):
        Question.objects.all().filter(id=question_id).delete()
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
        if request.data["idList"] is None:
            Auth.objects.all().delete()
            return Response({}, status=HTTP_200_OK)
        else:
            ids = get_ids(request.data["idList"])
            is_valid(len(ids) > 0, 'The format of the ids list is not correct')
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
        if request.data["idList"] is None:
            Key.objects.all().delete()
            return Response({}, status=HTTP_200_OK)
        else:
            ids = get_ids(request.data["idList"])
            is_valid(len(ids) > 0, 'The format of the ids list is not correct')
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
        if not serializer.is_valid():
            return Response({"result": "User object is not valid"}, status=HTTP_400_BAD_REQUEST)
        else:
            fields = request.data
            user = User(username=fields['username'], first_name=fields['first_name'],
                        last_name=fields['last_name'], email=fields['email'], is_staff=fields['is_staff'])
            user.set_password(request.data['password'])
            user.save()
            return Response({}, status=HTTP_200_OK)

    def delete(self, request):
        if request.data["idList"] is None:
            User.objects.all().filter(is_superuser=False).delete()
            return Response({}, status=HTTP_200_OK)
        else:
            ids = get_ids(request.data["idList"])
            is_valid(len(ids) > 0, 'The format of the ids list is not correct')
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
        ids = get_ids(request.data["idList"])
        state = request.data['state']
        value = request.data['value']
        is_valid(len(ids) > 0, 'The format of the ids list is not correct')
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
            res = Response({"result": "The field state must be Active, Staff or Superuser"}, status=HTTP_400_BAD_REQUEST)
        return res
