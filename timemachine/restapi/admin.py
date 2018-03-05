from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Problem)
admin.site.register(TestCase)
admin.site.register(Rating)
admin.site.register(Solution)
admin.site.register(User)
