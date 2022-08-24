from django.db import models

class User(models.Model): 
    name      = models.CharField(max_length=100)
    thumbnail = models.CharField(max_length=150)
    is_best   = models.BooleanField()
    rating    = models.ForeignKey('Rating', on_delete=models.CASCADE)

    class Meta:
        db_table = 'users'


class Rating(models.Model):
    name       = models.CharField(max_length=45)
    mark_image = models.CharField(max_length=150)

    class Meta:
        db_table = 'ratings'
