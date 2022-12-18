from django.db import models
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


class Students(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=12, blank=True, null=True)
    passw = models.CharField(max_length=30, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'students'


class Purchase(models.Model):
    id_class = models.ForeignKey(Class, models.DO_NOTHING, db_column='id_class')
    id_student = models.ForeignKey(Students, models.DO_NOTHING, db_column='id_student')
    date_of_order=models.DateField(blank=True, null=True)
    date_of_purchase = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'purchase'


# Create your models here.
