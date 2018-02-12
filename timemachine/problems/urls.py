from django.conf.urls import url
from problems import views

urlpatterns = [
    url(r'^$', views.problems_list),
    url(r'^(?P<pk>[0-9]+)/$', views.problems_detail),
]