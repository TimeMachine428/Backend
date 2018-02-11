
#"custom" imports
# url matches the URL in the browser to a module
# in your Django project
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index')
]
