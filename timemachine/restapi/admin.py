# from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import *

# register stuff to show on admin page
admin.site.register(Problem)
admin.site.register(Rating)
admin.site.register(Solution)
admin.site.register(User)

