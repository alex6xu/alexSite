# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# from django.contrib.sites.models import Site

# Create your models here.

class Tag(models.Model):
    tag_name = models.CharField(max_length=64)

    def __unicode__(self):
        return self.tag_name


class Article(models.Model):
    title = models.CharField(max_length = 100)  #博客题目
    author = models.ForeignKey(User, default=1, on_delete=models.SET_DEFAULT)
    category = models.CharField(max_length = 50, blank = True)  #博客分类 可为空
    tag = models.ManyToManyField(Tag, blank=True)  # 博客标签 可为空
    date_time = models.DateTimeField(auto_now_add = True)  #博客日期
    content = models.TextField(blank = True, null = True)  #博客文章正文
    count = models.IntegerField(default=0)

    def get_absolute_url(self):
        path = reverse('detail', kwargs={'id':self.id})
        return "http://127.0.0.1:8000%s" % path

    #python3使用__str__
    def __str__(self) :
        return self.title.encode('utf-8')

    class Meta:
        ordering = ['-date_time']

class Comment(models.Model):
    """
    评论
    """
    blog = models.ForeignKey(Article, verbose_name='博客', on_delete=models.DO_NOTHING)
    name = models.CharField('称呼', max_length=16)
    email = models.EmailField('邮箱')
    content = models.CharField('内容', max_length=240)
    created = models.DateTimeField('发布时间', auto_now_add=True)