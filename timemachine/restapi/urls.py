from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from restapi import views

urlpatterns = [
    url(r'^problem/(?P<pk>[0-9]+)/$', views.problem_detail),
    url(r'^problem/$', views.problem_list),
    url(r'^rating/(?P<pk>[0-9]+)/$', views.rating_detail),
    url(r'^rating/$', views.rating_list),
    url(r'^solution/(?P<pk>[0-9]+)/$', views.solution_detail),
    url(r'^solution/$', views.solution_list),
]

urlpatterns = format_suffix_patterns(urlpatterns)
