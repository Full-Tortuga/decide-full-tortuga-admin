from base import mods

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_302_FOUND
)
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages

from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView


from .serializers import UserSerializer
from django.urls import reverse
from django.db import models

import ldap
from decide.settings import AUTH_LDAP_SERVER_URI, AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD


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


class LDAPLogin(APIView):
    """
    Class to authenticate a user via LDAP and
    then creating a login session
    """

    def post(self, request):
        """
        Api to login a user
        :param request:
        :return:
        """
        try:
            # Probamos la conexion con el servidor con las siguientes instrucciones
            con = ldap.initialize(AUTH_LDAP_SERVER_URI)
            con.simple_bind_s(AUTH_LDAP_BIND_DN, AUTH_LDAP_BIND_PASSWORD)
            try:
                # Probamos a logear con los datos enviados por el usuario
                user_obj = authenticate(username=request.data['username'],
                                        password=request.data['password'])
                login(request, user_obj,
                      backend='django_auth_ldap.backend.LDAPBackend')

                # Añadir token al sesion para poder votar, en otro caso el votar con un usuario registrado con ldap resulta en un panic
                if user_obj and request.content_type == 'application/x-www-form-urlencoded':
                    user_data = {
                        'username': request.data['username'],
                        'password': request.data['password'],
                    }
                    token = mods.post('authentication',
                                      entry_point='/login/', json=user_data)
                    request.session['auth-token'] = token['token']

                return render(request, 'welcome.html', status=HTTP_200_OK)
            except AttributeError:
                return render(request, 'welcome.html', status=HTTP_400_BAD_REQUEST)
        except ldap.SERVER_DOWN:
            return render(request, 'welcome.html', status=HTTP_500_INTERNAL_SERVER_ERROR)


class SignInView(LoginView):
    template_name = 'form.html'


class RegisterUserView(APIView):
    def post(self, request):
        username = request.data.get('username', '')
        email = request.data.get('email', '')
        firstname = request.data.get('firstname', '')
        lastname = request.data.get('lastname', '')
        pwd = request.data.get('password', '')
        pwd2 = request.data.get('password2', '')
        if not pwd == pwd2:
            response = Response(
                {'error': 'Contraseñas no coinciden'}, HTTP_400_BAD_REQUEST)
            response['Location'] = reverse('sign_in')
            return response
        if User.objects.filter(username=username).count() > 0:
            response = Response({'error': 'Ya existe este nombre de usuario',
                                'username': username}, HTTP_400_BAD_REQUEST)
            response['Location'] = reverse('sign_in')
            return response

        try:
            user = User(username=username, email=email,
                        first_name=firstname, last_name=lastname)
            user.set_password(pwd)
            user.save()
            token, _ = Token.objects.get_or_create(user=user)
        except IntegrityError:
            return Response({}, status=HTTP_400_BAD_REQUEST)
        response = Response(
            {'user_pk': user.pk, 'token': token.key}, HTTP_302_FOUND)
        response['Location'] = reverse('sign_in')

        return response


class BienvenidaView(TemplateView):
    template_name = 'welcome.html'


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


def cerrarsesion(request):
    print("==========================LOGOUT========================")

    logout(request)
    messages.success(request, F"Su sesión se ha cerrado correctamente")
    return render(request, "welcome.html")


def landingpage(request):
    return render(request, "welcome.html")
