from django.contrib import admin

# Register your models here.
from .models import Tag, Article

admin.site.register([Article, Tag])