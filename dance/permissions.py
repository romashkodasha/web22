import logging

import redis
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.response import Response

from dance.models import User

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_staff or request.user.is_superuser))


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)
