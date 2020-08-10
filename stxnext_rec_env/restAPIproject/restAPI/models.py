from django.db import models
from django_mysql.models import ListCharField

class Book(models.Model):
    title = models.CharField(max_length=100, unique=True)
    authors = ListCharField(base_field=models.CharField(max_length=50), size=10, max_length=(50 * 11))
    published_date = models.CharField(max_length=10)
    categories = ListCharField(base_field=models.CharField(max_length=50), size=10, max_length=(50 * 11), default=None, null=True)
    average_rating = models.IntegerField(default=None, null=True)
    ratings_count = models.IntegerField(default=None, null=True)
    thumbnail = models.URLField(default=None, null=True)
    year = models.IntegerField()

    def __str__(self):
        return f'{self.title} published by {self.authors}'

    class Meta:
        ordering = ['year']
