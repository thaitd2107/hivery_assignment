"""hivery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from paranuara import apis
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('companies/', apis.company_list, name='companies'),
    path('companies/<int:pk>', apis.company_detail),
    path('peoples/<int:pk>', apis.people_detail, name='peoples'),
    url(r'^peoples/friends_in_common/$', apis.people_friends_in_common, name='friends-in-common'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
