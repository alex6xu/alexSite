# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.contrib import auth
from django.contrib.auth.models import User
import time
from django.template import RequestContext
# from django.views.decorators.csrf import csrf_protect
# from myuser.models import *
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from django import forms
# from django.contrib.sessions.models import Session
from .forms import *
from django.contrib.auth.decorators import login_required
from .models import Article
import logging

logger = logging.getLogger('django')


class IndexView(View):
    def get(self, request):
        logger.info('index view')
        jsr = {} # {'items': rec}
        return render(request, 'blog/index.html', jsr)


class UserRegister(View):
    def get(self,requset):
        rform= RegisterForm()
        return render(requset, 'blog/register.html', {'form':rform})

    def post(self,request):
        print('post register start')
        curtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

        try:
            rf = RegisterForm(request.POST)
            username = rf.data['username']
            password = rf.data['password1']

            if not rf.is_valid():
                errors = 'register not valid'
                return render_to_response("blog/success.html", RequestContext(request, {'curtime': curtime, 'errors': errors}))

            filterResult = User.objects.filter(username=username)
            if len(filterResult)>0:
                errors = "用户名已存在"
                return render_to_response("blog/success.html", RequestContext(request, {'curtime':curtime, 'errors':errors}))

            # print 'save user to db before'
            user=User()
            user.username=username
            user.set_password(password)
            user.email=rf.data['email']
            user.last_name = rf.data['phone']
            user.save()
            print('saved user info to db')

            newUser=auth.authenticate(username=username,password=password)
            if newUser is not None:
                auth.login(request, newUser)
                return HttpResponseRedirect("/blog/index")
        except Exception as e:
            errors = e
            return render_to_response("blog/success.html", RequestContext(request, {'curtime':curtime, 'errors':errors}))

        return render_to_response("blog/success.html", RequestContext(request, {'curtime':curtime}))


class LoginView(View):
    def get(self,request):
        lform = LoginForm()
        return render(request, 'blog/login.html', {'form': lform})

    def post(self,request):

        lf = LoginForm(request.POST)
        if not lf.is_valid():
            return HttpResponse({'res':0})

        username = lf.data['username']
        password = lf.data['password']
        jstr = {}
        try:
            # import pdb;pdb.set_trace()
            user = auth.authenticate(username=username, password=password)
            #user = User.objects.filter(username=username)
            print('user authenticated')
            if(user and user.is_active == 1):
                auth.login(request,user)
                result = 1
                jstr = {'result':result}
                # return HttpResponse(uu) #ajax
                return HttpResponseRedirect('/blog/index')

            elif(user and user.is_active != 1):
                #注册用户未激活
                errors = '注册用户未激活'
                print(errors)
                result = 2
                jstr = {'result':result, 'msg':errors}
                return HttpResponse(jstr)

            elif user is None:
                # 登录失败
                result = 3
                errors = '注册用户未激活'
                print(errors)
                jstr = {'result': result, 'msg': errors}
                return HttpResponse(jstr)
        except Exception as e:
            print(e)
            return HttpResponse({'res':0})


class AboutMe(View):
    def get(self,request):

        return render(request, 'blog/aboutme.html')


@login_required
def about_me(request):
    return render(request, 'blog/aboutme.html')


@login_required
def showPageList(request):
    if request.method == "GET":
        user = request.user
        # import pdb;pdb.set_trace()
        rec = Article.objects.filter(author=user)
        jsr = {'items':rec}
        return render(request, 'blog/showList.html', jsr)


class AddEssay(View):
    def get(self, request):

        return render(request, 'blog/add.html')

    def post(self, request):

        jstr={'result' : 'ok'}
        return HttpResponse(jstr)


def showUser(username):
    return HttpResponse('hello, %s' % username)


class AddComment(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


def showDetail(request):
    #show page detail and add artical count
    pass
