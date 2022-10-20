from django.shortcuts import render
from rest_framework import viewsets
from dance.serializers import GroupsSerializer
from dance.serializers import StudentsSerializer
from dance.serializers import SubscriptionsSerializer
from dance.serializers import TrainersSerializer
from dance.models import Groups
from dance.models import Students
from dance.models import Subscriptions
from dance.models import Trainers



class GroupsViewSet(viewsets.ModelViewSet):
    """
    API endpoint, который позволяет просматривать и редактировать группы
    """
    queryset = Groups.objects.all()
    serializer_class = GroupsSerializer  # Сериализатор для модели

class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer

class SubscriptionsViewSet(viewsets.ModelViewSet):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer

class TrainersViewSet (viewsets.ModelViewSet):
    queryset = Trainers.objects.all()
    serializer_class = TrainersSerializer

