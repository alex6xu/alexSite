# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest,JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.contrib.sessions.models import Session
from django.contrib import auth
from django.contrib.auth.models import User
import time
from django.template import RequestContext
# from myuser.models import *
from django import forms
from captcha.fields import CaptchaField
from django.contrib.auth.decorators import login_required
from models import Article

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码')
    captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名')
    email = forms.EmailField(label='email')
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2= forms.CharField(label='Confirm',widget=forms.PasswordInput)
    phone = forms.CharField(label='phone')
    captcha = CaptchaField(label='验证码')

class CommentForm(forms.Form):
    """
    评论表单
    """

    name = forms.CharField(label='称呼', max_length=16, error_messages={
        'required': '请填写您的称呼',
        'max_length': '称呼太长'
    })

    email = forms.EmailField(label='邮箱', error_messages={
        'required': '请填写您的邮箱',
        'invalid': '邮箱格式不正确'
    })

    content = forms.CharField(label='评论内容', error_messages={
        'required': '请填写您的评论内容',
        'max_length': '评论内容太长'
    })

# Create your views here.
class IndexView(View):
    # @login_required
    def get(self,request):

        return render(request, 'blog/index.html')

class UserRegister(View):
    def get(self,requset):
        rform= RegisterForm()
        return render(requset,'blog/register.html', {'form':rform})

    def post(self,request):
        print 'post register start'
        curtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

        try:
            rf = RegisterForm(request.POST)
            username = rf.data['username']
            password = rf.data['password1']

            if not rf.is_valid():
                errors = 'register not valid'
                return render_to_response("blog/success.html",RequestContext(request,{'curtime':curtime,'errors':errors}))

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
            print 'saved user info to db'

            newUser=auth.authenticate(username=username,password=password)
            if newUser is not None:
                auth.login(request, newUser)
                return HttpResponseRedirect("/blog/index")
        except Exception,e:
            errors = e
            return render_to_response("blog/success.html",RequestContext(request,{'curtime':curtime,'errors':errors}))

        return render_to_response("blog/success.html",RequestContext(request,{'curtime':curtime}))


class LoginView(View):
    def get(self,request):
        lform = LoginForm()
        return render(request,'blog/login.html', {'form': lform})

    def post(self,request):

        lf = LoginForm(request.POST)
        if not lf.is_valid():
            return HttpResponse({'res':0})

        username = lf.data['username']
        password = lf.data['password']
        jstr = {}
        try:
            import pdb;pdb.set_trace()
            user = auth.authenticate(username=username, password=password)
            #user = User.objects.filter(username=username)
            print 'user authenticated'
            if(user and user.is_active == 1):
                auth.login(request,user)
                result = 1
                jstr = {'result':result}
                # return HttpResponse(uu) #ajax
                return HttpResponseRedirect('/blog/index')

            elif(user and user.is_active != 1):
                #注册用户未激活
                errors = '注册用户未激活'
                print errors
                result = 2
                jstr = {'result':result, 'msg':errors}
                return HttpResponse(jstr)

            elif user is None:
                # 登录失败
                result = 3
                errors = '注册用户未激活'
                print errors
                jstr = {'result': result, 'msg': errors}
                return HttpResponse(jstr)
        except Exception, e:
            print e
            return HttpResponse({'res':0})


class AboutMe(View):
    def get(self,request):

        return render(request,'blog/aboutme.html')

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
        return render(request,'blog/showList.html', jsr)


class AddEssay(View):
    def get(self,request):

        return render(request,'blog/add.html')

    def post(self,request):

        jstr={'result' : 'ok'}
        return HttpResponse(jstr)

def showUser(username):
    return HttpResponse('hello, %s' % username)


class AddComment(View):
    def get(self,request):
        pass

    def post(self,request):
        pass


def showDetail(request):
    #show page detail and add artical count
    pass