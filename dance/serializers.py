from dance.models import Class, Purchase, User
from rest_framework import serializers

from django.contrib.auth import authenticate

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Class
        # Поля, которые мы сериализуем
        fields = ["id", "trainer", "date", "price", "place","descr","img","status"]

# class StudentsSerializer (serializers.ModelSerializer):
#     class Meta:
#         model = Students
#         fields = ["id", "name", "phone", "passw"]

class PurchaseSerializer (serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ["id", "id_class", "id_student", "date_of_order", "date_of_purchase","status"]

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(max_length=128, write_only=True)

    # Ignore these fields if they are included in the request.

    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    birth_date = serializers.DateField(read_only=True)
    sex = serializers.CharField(read_only=True)

    def validate(self, data) -> User:
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError(
                'A username address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.'
            )

        return user


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=4,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'phone', 'is_staff', 'is_superuser', 'birth_date')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['id', 'email', 'username', 'birth_date']