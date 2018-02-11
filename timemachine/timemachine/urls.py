"""timemachine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Loads URLs for Admin site
from django.contrib import admin

#idk, but was there already
from django.urls import path


#"custom" imports
# url matches the URL in the browser to a module
# in your Django project
from django.conf.urls import url

# 3 include allows you to reference other url files
# in our project
from django.conf.urls import include

# Reference the fuctions in the views.py file
from timemachine.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^helloworld/$', hello_world),
    url(r'^$', root_page),
    url(r'^html/$', html),
    url(r'^reviewrating/', include('reviewrating.urls'))
]
