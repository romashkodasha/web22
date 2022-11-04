from django.shortcuts import render
from rest_framework import viewsets
from dance.serializers import ClassSerializer
from dance.serializers import StudentsSerializer
from dance.serializers import PurchaseSerializer
from dance.models import Class
from dance.models import Students
from dance.models import Purchase



class ClassesViewSet(viewsets.ModelViewSet):
    """
    API endpoint, который позволяет просматривать и редактировать группы
    """
    queryset = Class.objects.all()
    serializer_class = ClassSerializer  # Сериализатор для модели

class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


