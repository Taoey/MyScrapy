from django.db import models

# Create your models here.


class People(models.Model):
    name=models.CharField(max_length=30)
    QQEmail=models.CharField(max_length=25)
    age=models.IntegerField()


