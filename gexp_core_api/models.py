from __future__ import unicode_literals

from django.core.validators import URLValidator
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ('name',)

class Subcategory(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)


class Indicator(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    subcategory = models.ForeignKey(Subcategory, related_name='indicators', on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)


class Country(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    dbpedia_url = models.CharField(max_length=2000, validators=[URLValidator()])
    smth = models.CharField(max_length=100, default='')

    class Meta:
        ordering = ('name',)

