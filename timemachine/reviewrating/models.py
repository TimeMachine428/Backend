from django.db import models

import datetime
from django.utils import timezone

# Create your models here.

class Rating(models.Model):
	
	#WHY TF we don't have a contructor?


	#attributes for database
	title = models.CharField(max_length = 200)
	date = models.DateTimeField('review date')
	rating = models.PositiveSmallIntegerField()
	content = models.CharField(max_length = 2000)
	