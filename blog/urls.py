# -*- coding:utf-8 -*-
# __author__ = 'alex'
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='main'),
    url(r'^index', IndexView.as_view(), name='index'),
    url(r'^login', LoginView.as_view(), name='login'),
    url(r'^aboutme', about_me, name='aboutme'),
    url(r'^register', UserRegister.as_view(),name='register'),
    url(r'^add', AddEssay.as_view(),name='addessay'),
    url(r'^showlist', showPageList,name='showPageList'),
    # url(r'^(?P<username>(\w+))',showUser, name='showUser'),
]
