import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

# Create your models here.
class Question(models.Model):
	title = models.CharField('title', max_length=200, blank=False)
	programming_language = models.CharField('programming language', max_length=100, blank=False)
	level = models.IntegerField(
		'level',
		validators=[
			MaxValueValidator(5),
			MinValueValidator(1)
			]
		)
	description = models.TextField('description', blank=False)
	solution = models.TextField('solution', blank=False)
	pub_date = models.DateTimeField('date published')

	def __str__(self):
		return self.title
	def was_published_last_week(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=7)
