from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.


class Problem(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    author = models.CharField(max_length=100, blank=True, default='')
    description = models.CharField(max_length=100, blank=True, default='')
    difficulty = models.IntegerField()
    good = models.IntegerField()

    class Meta:
        ordering = ('difficulty',)


class Rating(models.Model):
    title = models.CharField(max_length = 200)
    date = models.DateTimeField('review date')
    rating = models.PositiveSmallIntegerField(
        'user rating',
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ]
    )
    content = models.CharField(max_length = 2000)

    class Meta:
        ordering = ('date',)


class Solution(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    code = models.TextField()
    language = models.CharField(default='python', max_length=100)
    output = models.TextField()
    pending = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
