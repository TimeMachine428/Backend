from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from problems import views

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.problems_detail),
    url(r'^$', views.problems_list),
]

urlpatterns = format_suffix_patterns(urlpatterns)
