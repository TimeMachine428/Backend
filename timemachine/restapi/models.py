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
