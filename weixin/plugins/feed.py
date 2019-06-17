#coding=utf-8
import feedparser
from alexSite.utils import ObjectDict
from django.conf import settings

__name__ = 'feed'


def test(data, msg=None, bot=None):
    if not settings.FEED_URL:
        return False
    if 'rss feed' in data or '博客更新' in data:
        return True
    return False


def respond(data, msg=None, bot=None):
    parser = feedparser.parse(settings.FEED_URL)
    articles = []
    i = 0
    for entry in parser.entries:
        if i > 9:
            break
        article = ObjectDict()
        article.title = entry.title
        article.description = entry.description[0:100]
        article.url = entry.link
        article.picurl = ''
        articles.append(article)
        i += 1
    return articles
