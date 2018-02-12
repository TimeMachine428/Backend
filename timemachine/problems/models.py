from django.db import models

# Create your models here.

class Problem(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    author = models.CharField(max_length=100, blank=True, default='')
    description = models.CharField(max_length=100, blank=True, default='')
    difficulty = models.IntegerField()
    good = models.IntegerField()

    class Meta:
        ordering = ('difficulty',)