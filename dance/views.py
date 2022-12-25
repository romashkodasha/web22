from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework import filters
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from django.db.models import Max, Min
from rest_framework.views import APIView

from dance.serializers import ClassSerializer, PurchaseSerializer, LoginSerializer, RegistrationSerializer, \
    UserSerializer
from dance.models import Class, User, Purchase
from django.conf import settings
import redis
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import uuid
import logging
from dance.permissions import IsStaff, IsSuperUser
from rest_framework.generics import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


class ClassesViewSet(viewsets.ModelViewSet):
    """
    API endpoint, который позволяет просматривать и редактировать группы
    """
    serializer_class = ClassSerializer  # Сериализатор для модели
    filter_backends = [filters.SearchFilter]
    search_fields = ['trainer']

    def get_permissions(self):
        if self.action in ['list', 'price_range', 'retrieve']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action in ['post', 'create', 'update', 'partial_update']:
            permission_classes = [IsStaff]
        else:
            permission_classes = [IsSuperUser]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        serializer = ClassSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        queryset = Class.objects.all()
        service = get_object_or_404(queryset, pk=pk)
        serializer = ClassSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        request_service = request.data
        service_serialized = ClassSerializer(request_service)
        request_service.save()
        return Response(service_serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, **kwargs):
        try:
            service = Class.objects.get(pk=pk)
        except Class.DoesNotExist:
            return Response({'message': 'The services does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClassSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, **kwargs):
        try:
            self.get_queryset().delete()
        except Exception:
            return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def price_range(self, request):
        classes = self.get_queryset()
        try:
            return Response(classes.aggregate(price_min=Min('price'), price_max=Max('price')))
        except:
            return Response([], status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self):
        queryset = Class.objects.filter(status=True)
        min_price = self.request.query_params.get('minPrice')
        max_price = self.request.query_params.get('maxPrice')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        return queryset


class PurchaseViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer

    def get_permissions(self):
        if self.action in ['list', 'partial_update', 'destroy', 'create', 'purchase_statuses']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action in ['retrieve', 'update', 'create']:
            permission_classes = [IsStaff]
        else:
            permission_classes = [IsSuperUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Purchase.objects.all().order_by('id')
        user_id = self.request.query_params.get('user_id')
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        if user_id:
            queryset = queryset.filter(id_student=user_id)
        return queryset

    @action(detail=False, methods=['get'])
    def purchase_statuses(self, request):
        statuses = []
        for choice in Purchase.PurchaseStatus.choices:
            statuses.append({'value': choice[0], 'label': choice[1]})
        try:
            return Response(statuses)
        except:
            return Response([], status=status.HTTP_404_NOT_FOUND)
    def list(self, request, *args, **kwargs):
        serializer = PurchaseSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        queryset = Purchase.objects.all()
        contract = get_object_or_404(queryset, pk=pk)
        serializer = PurchaseSerializer(contract)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        request_purchase = request.data
        purchase_serialized = PurchaseSerializer(request_purchase)
        request_purchase.save()
        return Response(purchase_serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, **kwargs):
        try:
            contract = Purchase.objects.get(pk=pk)
        except Purchase.DoesNotExist:
            return Response({'message': 'The purchase does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseSerializer(contract, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, **kwargs):
        try:
            Purchase.objects.get(pk=pk).delete()
        except Exception:
            return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        user = User.objects.get(username=serializer.data.get('username'))
        random_key = str(uuid.uuid4())
        response.set_cookie(key='session_id', value=random_key, samesite='None', secure=True)
        session_storage.set(random_key, value=user.pk)
        return response


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"status": "registration successful"}, status=status.HTTP_201_CREATED)


class LogoutAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        session_id = request.COOKIES.get('session_id')
        if session_id:
            session_storage.delete(session_id)
            response = Response({"status": "logout"}, status=status.HTTP_200_OK)
            response.delete_cookie('session_id')
            return response

        return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in []:
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsStaff]
        else:
            permission_classes = [IsSuperUser]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        queryset = User.objects.all()
        contract = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(contract)
        return Response(serializer.data, status=status.HTTP_200_OK)