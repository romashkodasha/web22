from dance.models import Groups
from dance.models import Students
from dance.models import Subscriptions
from dance.models import Trainers
from rest_framework import serializers


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Groups
        # Поля, которые мы сериализуем
        fields = ["id", "style", "age", "id_trainer","pic"]

class StudentsSerializer (serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ["id", "name", "phone", "birth_date"]

class SubscriptionsSerializer (serializers.ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = ["id", "id_group", "id_student", "num_classes", "date_of_purchase","status"]

#справочные таблицы
class TrainersSerializer (serializers.ModelSerializer):
    class Meta:
        model = Trainers
        fields = ["id", "name", "info", "phone","photo", "birth_date" ]