from django.db import models
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

from dance.managers import UserManager


# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_student = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user'


# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user_id = models.BigIntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)

#
# class DjangoMigrations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'django_migrations'
#
# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'django_session'

class Class(models.Model):
    trainer = models.CharField(max_length=30)
    date = models.DateTimeField()
    price = models.IntegerField(blank=True, null=True)
    place = models.CharField(max_length=50, blank=True, null=True)
    descr = models.CharField(max_length=255, blank=True, null=True)
    img = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'classes'

    def __str__(self):
        return self.trainer


class Purchase(models.Model):
    PurchaseStatus = [
        ('BOOKED', 'booked'),
        ('PAID', 'paid'),
        ('PASSED', 'passed'),
    ]
    id_class = models.ForeignKey(Class, models.DO_NOTHING, db_column='id_class')
    id_student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchase',
                                   related_query_name='purchase', db_column='id_student')
    date_of_order = models.DateField(blank=True, null=True)
    date_of_purchase = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=PurchaseStatus, null=True)

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


# class DanceUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#
#     class Meta:
#         managed = True
#         db_table = 'dance_user_groups'
#         unique_together = (('user', 'group'),)
#
#
# class DanceUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)
#
#     class Meta:
#         managed = True
#         db_table = 'dance_user_permissions'
#         unique_together = (('user', 'permission'),)
