from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from restapi import views

urlpatterns = [
    url(r'^problems/(?P<pk>[0-9]+)/$', views.problems_detail),
    url(r'^problems/$', views.problems_list),
]

urlpatterns = format_suffix_patterns(urlpatterns)
