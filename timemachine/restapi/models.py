from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import datetime
import json


# Create your models here.


class Problem(models.Model):
    title = models.CharField('title', max_length=200, blank=False)
    programming_language = models.CharField('programming language', max_length=100, blank=False)
    author = models.ForeignKey('User', on_delete=models.CASCADE, null=True, related_name='problems')
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
        ],
        null=True
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def was_published_last_week(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=7)

    @property
    def owner(self):
        return self.author

    class Meta:
        ordering = ('difficulty',)


class TestCase(models.Model):
    method = models.CharField(max_length=200, blank=False)
    inputs = models.TextField(default="[]")
    outputs = models.TextField(default="[]")
    problem = models.ForeignKey(to=Problem, on_delete=models.CASCADE, related_name='test_cases')

    def __str__(self):
        input_array = json.loads(self.inputs)
        output_tuple = json.loads(self.outputs)
        return "%s: %s(%s)==%s" % (self.problem.title,
                                   self.method,
                                   ', '.join('%s' % i for i in input_array),
                                   ', '.join('%s' % i for i in output_tuple))

    @property
    def owner(self):
        return self.problem.owner


class Rating(models.Model):
    message = models.CharField(max_length=300)
    date = models.DateTimeField('review date', auto_now_add=True)
    rating = models.PositiveSmallIntegerField(
        'user rating',
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    content = models.CharField(max_length=2000)
    rating_of = models.ForeignKey('Problem', on_delete=models.CASCADE, related_name='ratings', null=True)
    reviewer = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='ratings', null=True)

    class Meta:
        ordering = ('date',)

    @property
    def owner(self):
        return self.reviewer


class Solution(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    code = models.TextField()
    language = models.CharField(default='python', max_length=100)
    output = models.TextField()
    author = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='solutions')
    problem = models.ForeignKey('Problem', on_delete=models.CASCADE, null=True, related_name='solutions')

    class Meta:
        ordering = ('created',)


class User(AbstractUser):
    github_id = models.IntegerField(null=True)
