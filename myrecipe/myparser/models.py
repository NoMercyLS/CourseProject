from django.db import models


# Create your models here.

class Recipe(models.Model):
    title = models.CharField('title', max_length=50)
    calories_amount = models.IntegerField('calories_amount')
    serving_count = models.IntegerField('serving_count')
    cooking_time = models.IntegerField('cooking_time')
    src = models.URLField('src_url')
    image = models.URLField('image_url')
