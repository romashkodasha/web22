from django.db import models
class Groups(models.Model):
    style = models.CharField(max_length=30, blank=True, null=True)
    age = models.CharField(max_length=10, blank=True, null=True)
    id_trainer = models.ForeignKey('Trainers', models.DO_NOTHING, db_column='id_trainer')
    pic = models.CharField(max_length=500, blank=True, null=True)
    timetable=models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'groups'


class Students(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=12, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'students'


class Subscriptions(models.Model):
    id_group = models.ForeignKey(Groups, models.DO_NOTHING, db_column='id_group')
    id_student = models.ForeignKey(Students, models.DO_NOTHING, db_column='id_student')
    num_classes = models.IntegerField(blank=True, null=True)
    date_of_purchase = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'subscriptions'


# class Timetable(models.Model):
#     id_group = models.ForeignKey(Groups, models.DO_NOTHING, db_column='id_group')
#     day = models.CharField(max_length=15, blank=True, null=True)
#     time = models.TimeField(blank=True, null=True)
#
#     class Meta:
#         managed = True
#         db_table = 'timetable'


class Trainers(models.Model):
    name = models.CharField(max_length=50)
    info = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    photo = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trainers'
# Create your models here.
