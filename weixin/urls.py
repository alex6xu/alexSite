from django.urls import include, path
from .views import *

urlpatterns = [
    path('index/', Index, name='main-view'),
    path('notify', Info, name='info'),
    # path('articles/<slug:title>/', views.article, name='article-detail'),
    # path('articles/<slug:title>/<int:section>/', views.section, name='article-section'),
    path('test/', Test, name='test'),
    ...
]