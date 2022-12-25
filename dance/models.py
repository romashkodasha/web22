from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from dance.managers import UserManager


class Class(models.Model):
    trainer = models.CharField(max_length=30)
    date = models.DateTimeField()
    price = models.IntegerField(blank=True, null=True)
    place = models.CharField(max_length=50, blank=True, null=True)
    descr = models.CharField(max_length=255, blank=True, null=True)
    img = models.CharField(max_length=500, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'classes'

    def __str__(self):
        return self.trainer


class Purchase(models.Model):
    class PurchaseStatus(models.TextChoices):
        BOOKED = 'BOOKED', ('Забронирован')
        PAID = 'PAID', ('Оплачен')
        PASSED = 'PASSED', ('Пройден')

    id_class = models.ForeignKey(Class, models.DO_NOTHING, db_column='id_class')
    id_student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchase',
                                   related_query_name='purchase', db_column='id_student')
    date_of_order = models.DateField(blank=True, null=True)
    date_of_purchase = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=PurchaseStatus.choices, null=True)

    class Meta:
        managed = True
        db_table = 'purchase'


class User(AbstractBaseUser, PermissionsMixin):
    password = models.CharField(max_length=128, null=True)
    username = models.CharField(db_index=True, max_length=255, unique=True, null=True)
    email = models.EmailField(db_index=True, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=12, null=True)
    is_staff = models.BooleanField(default=False)

    birth_date = models.DateField(default='1999-01-01')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'birth_date']

    objects = UserManager()

    class Meta:
        managed = True
        db_table = 'user'

    def __str__(self):
        return self.username

