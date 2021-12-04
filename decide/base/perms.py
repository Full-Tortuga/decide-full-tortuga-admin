from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import permissions, exceptions
from rest_framework.authtoken.models import Token

from base import mods


class UserIsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.auth:
            return False
        response = mods.post('authentication/getuser', json={'token': request.auth.key},
                             response=True)
        return response.json().get('is_staff', False)


class IsAdminAPI(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        key = request.COOKIES.get('token', "")
        try:
            tk = get_object_or_404(Token, key=key)
        except Http404:
            raise exceptions.PermissionDenied(detail="You are not logged in")
        return tk.user.is_superuser
