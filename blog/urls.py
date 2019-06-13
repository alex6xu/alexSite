# -*- coding:utf-8 -*-
# __author__ = 'alex'
from django.conf.urls import url
from django.urls import path
from .views import *

app_name ='[blog]'
urlpatterns = [
    path(r'', IndexView.as_view(), name='main'),
    path(r'index', IndexView.as_view(), name='index'),
    path(r'login', LoginView.as_view(), name='login'),
    path(r'aboutme', about_me, name='aboutme'),
    path(r'register', UserRegister.as_view(),name='register'),
    path(r'add', AddEssay.as_view(),name='addessay'),
    path(r'showlist', showPageList,name='showPageList'),
    # url(r'^(?P<username>(\w+))',showUser, name='showUser'),
]
