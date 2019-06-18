from django.urls import include, path
from .views import *
from django.views.decorators.csrf import csrf_exempt


app_name = "weixin"
urlpatterns = [
    path('index', Index.as_view(), name='main-view'),
    path('notify', csrf_exempt(Notify.as_view()), name='notify'),
    path('call', csrf_exempt(Info.as_view()), name='info'),
    # path('articles/<slug:title>/', views.article, name='article-detail'),
    # path('articles/<slug:title>/<int:section>/', views.section, name='article-section'),
    path('test', Test.as_view(), name='test'),
]