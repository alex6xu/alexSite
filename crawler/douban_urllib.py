#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# @Date    : 2016-09-06
# @Author  : Alex

import re
import urllib
import urllib2
import cookielib
import random
import time
import logging
import socket
from bs4 import BeautifulSoup

# import mysqldb

socket.setdefaulttimeout(5)

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='douban.log',
                filemode='w')

email = '*****@163.com'
password = '******'
cookies_file = 'Cookies.txt'


class DoubanClient(object):

    def __init__(self):
        self.email = email
        self.password = password
        self.data = {
            "form_email": email,
            "form_password": password,
            "source": "index_nav",
            "remember": "on"
        }

        self.login_url = 'https://www.douban.com/accounts/login'
        self.load_cookies()
        self.opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(self.cookie))
        self.opener.addheaders = [("User-agent", "Mozilla/5.0 (X11; Linux x86_64)\
          AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36")]
        # self.opener.addheaders = [("Origin", "https://www.douban.com")]
        self.get_ck()

    def load_cookies(self):
        try:
            self.cookie = cookielib.MozillaCookieJar()
            self.cookie.load(cookies_file)
            logging.info( "loading cookies for file...")
        except Exception as e:

            logging.info( "The cookies file is not exist.")
            self.login_douban()
            # reload the cookies.
            self.load_cookies()

    def get_ck(self):
        # open a url to get the value of ck.
        self.opener.open('https://www.douban.com')
        # read ck from cookies.
        for c in list(self.cookie):

            if c.name == 'ck':
                self.ck = c.value.strip('"')
                logging.info( "ck:%s" % self.ck)
                break
        else:
            logging.info( 'ck is end of date.')
            self.login_douban()
            # #reload the cookies.
            self.cookie.revert(cookies_file)
            self.get_ck()

    def login_douban(self):
        '''
        login douban and save the cookies into file.

        '''
        cookieJar = cookielib.MozillaCookieJar(cookies_file)
        # will create (and save to) new cookie file

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
        #!!! following urllib2 will auto handle cookies
        response = opener.open(self.login_url, urllib.urlencode(self.data))
        html = response.read()
        regex = r'<img id="captcha_image" src="(.+?)" alt="captcha"'
        imgurl = re.compile(regex).findall(html)
        if imgurl:
            # urllib.urlretrieve(imgurl[0], 'captcha.jpg')
            print("The captcha_image url address is %s" % imgurl[0])
            logging.info("The captcha_image url address is %s" % imgurl[0])
            # download the captcha_image file.
            # data = opener.open(imgurl[0]).read()
            # f = file("captcha.jpg","wb")
            # f.write(data)
            # f.close()

            captcha = re.search(
                '<input type="hidden" name="captcha-id" value="(.+?)"/>', html)
            if captcha:
                vcode = input('图片上的验证码是：')
                self.data["captcha-solution"] = vcode
                self.data["captcha-id"] = captcha.group(1)
                self.data["user_login"] = "登录"
                # 验证码验证
                response = opener.open(
                    self.login_url, urllib.urlencode(self.data))
                # fp = open("2.html","wb")
                # fp.write(response.read())
                # fp.close

        # 登录成功
        cookieJar.save()
        if response.geturl() == "http://www.douban.com/":
            logging.info( 'login success !')
            # update cookies, save cookies into file
            # cookieJar.save();
        else:
            return False
        return True

    def new_topic(self, group_id, title, content):

        group_url = "https://www.douban.com/group/" + group_id
        post_url = group_url + "/new_topic"
        post_data = urllib.urlencode({
            'ck': self.ck,
            'rev_title': title,
            'rev_text': content,
            'rev_submit': '好了，发言',
        })
        request = urllib2.Request(post_url)

        # request.add_header("Origin", "https://www.douban.com")
        request.add_header("Referer", post_url)
        response = self.opener.open(request, post_data)
        if response.geturl() == group_url:
            logging.info( 'Okay, Success !')
            return True
        return False

    def talk_statuses(self, content='(⊙o⊙)…'):

        post_data = urllib.urlencode({
            'ck': self.ck,
            'comment': content,
        })

        request = urllib2.Request("https://www.douban.com/")
        # request.add_header("Origin", "https://www.douban.com")
        request.add_header("Referer", "https://www.douban.com/")
        self.opener.open(request, post_data)

    def send_mail(self, id, content='Hey,girl !'):

        post_data = urllib.urlencode({
            "ck": self.ck,
            "m_submit": "好了，寄出去",
            "m_text": content,
            "to": id,
        })
        request = urllib2.Request("https://www.douban.com/doumail/write")
        # request.add_header("Origin", "https://www.douban.com")
        request.add_header("Referer", "https://www.douban.com/doumail/write")
        self.opener.open(request, post_data)

    def sofa(self,
             group_id,
             content=['丫鬟命，公主心，怪不得人。',
                      '要交流就平等交流，弄得一副跪舔样,谁还能瞧得起你？',
                      '己所欲，勿施于人..',
                      '人在做，天在看.', ]
             ):

        group_url = "https://www.douban.com/group/" + group_id + "/#topics"
        html = self.opener.open(group_url).read()
        topics = re.findall(r'topic/(\d+?)/.*?class="">.*?<td nowrap="nowrap" class="">(.*?)</td>',
                            html, re.DOTALL)

        for item in topics:
            if item[1] == '':
                post_data = urllib.urlencode({
                    "ck": self.ck,
                    "rv_comment": random.choice(content),
                    "start": "0",
                    "submit_btn": "加上去"
                })
                self.opener.open(
                    "https://www.douban.com/group/topic/" + item[0] + "/add_comment#last?", post_data)

    def get_joke(self):
        html = urllib2.urlopen('http://www.xiaohuayoumo.com/').read()
        result = re.compile(
            r']<a href="(.+?)">(.+?)</a></div>.+?', re.DOTALL).findall(html)
        for x in result[:1]:
            title = x[1]
            joke_url = 'http://www.xiaohuayoumo.com' + x[0]
            page = self.opener.open(joke_url).read()
            result = re.compile(r'content:encoded">(.+?)<p.+?</p>(.+?)</div></div></div></div>',
                                re.DOTALL).findall(page)
            for x in result[:1]:
                content = x[0] + x[1]
                content = re.sub(r'</?\w+[^>]*>', ' ', content)

        return title, content

    def get_group_list(self, group_url):
        try:
            html = self.opener.open(group_url).read()
        except Exception as e:
            logging.exception('open group list [%s] failed' % group_url)
            return None

        # print html
        soup = BeautifulSoup(html, 'lxml')
        # images = re.findall(r'<td class="td-subject">(.*?)</td>', html, re.DOTALL)
        subjects = soup.find_all("td",{'class':"td-subject"})
        logging.info( 'get urls')
        # import pdb; pdb.set_trace()
        urls = [x.a.get('href') for x in subjects]
        return urls

    def download_pic(self, html):
        # def download(html):
        soup = BeautifulSoup(html, 'lxml')
        # i = 1
        download_img = None
        for k in soup.find_all('div', {'class': 'topic-figure cc'}):
            url = k.img.get('src')
            img_numlist = re.findall(r'p\d{8}', url)
            for img_num in img_numlist:
                try:
                    download_img = urllib.urlretrieve(url, 'download/%s.jpg' % img_num)
                except IOError as e:
                    logging.exception(e)

                # time.sleep(0.5)
                # i += 1
                logging.info(url)

        # return download_img

    def crawler(self, group_url, num):
        urls = self.get_group_list(group_url)
        for u in urls:
            try:
                ht = self.opener.open(u).read()
            except:
                logging.warn('open topics [%s] failed ' % u)
                continue
            self.download_pic(ht)
            logging.info( u + ' finished')
            time.sleep(1)
        logging.info('download  page %s finished !' % num)

    def run(self):
        # group_url = "https://www.douban.com/group/"
        # self.crawler(group_url, 0)
        for num in range(1000, 2000, 50):
            group_url = "https://www.douban.com/group/" + "?start=%s" % num # + group_id + "/#topics"
            self.crawler(group_url, num)



def main():
    app = DoubanClient()

    # titile, content = app.get_joke()
    # if titile and content:
    #     print app.new_topic("cd", titile, content)

    # app.send_mail(81790757, content)
    # app.talk_statuses('Hello.it\'s a test message using python.')
    # app.sofa("CentOS")
    app.run()


if __name__ == '__main__':
    main()
