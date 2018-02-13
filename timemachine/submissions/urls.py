from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit),
    path('job/', views.get_job),
]
