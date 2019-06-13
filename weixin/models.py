
from __future__ import unicode_literals
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# from django.contrib.sites.models import Site

# Create your models here.

class WXUser(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    active = models.BooleanField()
    phone = models.CharField(max_length=16)
    access_token = models.CharField(max_length=255)
    openid = models.CharField(max_length=64)
    refresh_token = models.CharField(max_length=255)
    expire_time = models.DateTimeField()

    def __unicode__(self):
        return self.openid
