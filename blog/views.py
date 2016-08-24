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

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    captcha = CaptchaField()


class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2= forms.CharField(label='Confirm',widget=forms.PasswordInput)
    captcha = CaptchaField()


# Create your views here.
class IndexView(View):
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
            # print 'get post params '
            errors = ''
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

        username = request.POST.get('username')
        password = request.POST.get('password')
        lf = LoginForm(request.POST)
        if not lf.is_valid():
            return HttpResponse({'res':0})

        uu = {}
        try:
            import pdb;pdb.set_trace()
            user = auth.authenticate(username=username, password=password)
            #user = User.objects.filter(username=username)

            if(user and user.is_active == 1):
                auth.login(request,user)
                result = 1

                uu = {'res':result}
                # return HttpResponse(uu) #ajax
                return HttpResponseRedirect('/blog/index')
        except Exception, e:
            print e
            return HttpResponse({'res':0})



class AboutMe(View):
    def get(self,request):

        return render(request,'blog/aboutme.html')

class ShowPageList(View):
    def get(self,request):

        return render(request,'')

    def post(self,request):

        return render(request,'')

class AddEssay(View):
    def get(self,request):

        return render(request,'blog/add.html')

    def post(self,request):

        jstr={'result' : 'ok'}
        return HttpResponse(jstr)

def showUser(username):
    return HttpResponse('hello, %s' % username)