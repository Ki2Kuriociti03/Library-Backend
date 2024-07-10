from django.db import models


class Book(models.Model):
     name = models.CharField(max_length=200)
     author = models.CharField(max_length=200)
     year = models.IntegerField()
     rating = models.IntegerField()
     isbn = models.CharField(max_length=20)
     quantity = models.IntegerField()
     tags = models.CharField(max_length=200)
