# -*- coding:utf-8 -*-

__author__ = 'alex'
from django.conf.urls import url,include
from django.contrib import admin
from views import *

urlpatterns = [
    url(r'^index', IndexView.as_view(),name='index'),
    url(r'^login', LoginView.as_view(),name='login'),
    url(r'^aboutme', LoginView.as_view(),name='aboutme'),
    url(r'^register', UserRegister.as_view(),name='register'),
    url(r'^add', AddEssay.as_view(),name='addessay'),
    url(r'^showlist', ShowPageList.as_view(),name='showPageList')
]
