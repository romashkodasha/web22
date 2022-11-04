from dance.models import Class
from dance.models import Students
from dance.models import Purchase
from rest_framework import serializers
class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Class
        # Поля, которые мы сериализуем
        fields = ["id", "trainer", "date", "place","deskr","img"]

class StudentsSerializer (serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ["id", "name", "phone", "mail", "passw"]

class PurchaseSerializer (serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ["id", "id_class", "id_student", "date_of_order", "date_of_purchase","status"]
