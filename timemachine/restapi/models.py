from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
import datetime


# Create your models here.


class Problem(models.Model):
    title = models.CharField('title', max_length=200, blank=False)
    programming_language = models.CharField('programming language', max_length=100, blank=False)
    author = models.OneToOneField('User', on_delete=models.CASCADE, null=True)
    description = models.TextField('description', blank=False)
    difficulty = models.IntegerField(
        'difficulty',
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    rating = models.IntegerField(
        'rating',
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title

    def was_published_last_week(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=7)

    class Meta:
        ordering = ('difficulty',)


class TestCase(models.Model):
    method = models.CharField(max_length=200, blank=False)
    inputs = models.TextField(default="[]")
    outputs = models.TextField(default="[]")
    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE)


class Rating(models.Model):
    message = models.CharField(max_length=300)
    date = models.DateTimeField('review date')
    rating = models.PositiveSmallIntegerField(
        'user rating',
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    content = models.CharField(max_length=2000)

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


class User(models.Model):
    github_id = models.IntegerField(blank=False)
    temp_usr = models.CharField('username', max_length=60, blank=False)

    def __str__(self):
        return self.temp_usr
