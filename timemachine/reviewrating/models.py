from django.db import models

import datetime
from django.utils import timezone

# Create your models here.

class Rating(models.Model):
	
	#WHY TF we don't have a contructor?


	#attributes for database
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


	def __str__(self):
		 """String representation of a user rating of a problem."""
		return self.title
	def is_a_good_rating(self):
		return self.rating >= 4
