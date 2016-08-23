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

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2= forms.CharField(label='Confirm',widget=forms.PasswordInput)
    def is_validate(self):
        return self.data['password1'] == self.data['password2']


# Create your views here.
class IndexView(View):
    def get(self,request):

        return render(request, 'blog/index.html')

class UserRegister(View):
    def get(self,requset):

        return render(requset,'blog/register.html')

    def post(self,request):
        print 'post register start'
        curtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

        # if request.user.is_authenticated():#a*******************
        #     print 'user authenticated !'
        #     return HttpResponseRedirect("/user")
        try:
            if request.method=='POST':
                print 'get post params '
                username=request.POST.get('username','')
                password1=request.POST.get('pwd','')
                password2=request.POST.get('pwd2','')
                email=request.POST.get('email','')
                phone=request.POST.get('phone','')
                errors=[]

                registerForm = RegisterForm({'username':username,'password1':password1,'password2':password2,'email':email})#b********
                if not registerForm.is_validate():
                    errors.extend(registerForm.errors.values())
                    print 'register not valid'
                    return render_to_response("register.html",RequestContext(request,{'curtime':curtime,'username':username,'email':email,'errors':errors}))
                if password1!=password2:
                    errors.append("两次输入的密码不一致!")
                    print 'pwd not same'
                    return render_to_response("register.html",RequestContext(request,{'curtime':curtime,'username':username,'email':email,'errors':errors}))

                filterResult = User.objects.filter(username=username)
                if len(filterResult)>0:
                    errors.append("用户名已存在")
                    return render_to_response("register.html",RequestContext(request,{'curtime':curtime,'username':username,'email':email,'errors':errors}))

                print 'save user to db before'
                user=User()
                user.username=username
                user.set_password(password1)
                user.email=email
                user.save()
                print 'saved user info to db'
                #用户扩展信息 profile
                # profile=AuthUser()
                # profile.user_id=user.id
                # profile.phone=phone
                # profile.save()
                #登录前需要先验证
                newUser=auth.authenticate(username=username,password=password1)
                if newUser is not None:
                    auth.login(request, newUser)#g*******************
                    return HttpResponseRedirect("/blog/index")
        except Exception,e:
            errors.append(str(e))
            return render_to_response("register.html",RequestContext(request,{'curtime':curtime,'username':username,'email':email,'errors':errors}))

        return render_to_response("register.html",RequestContext(request,{'curtime':curtime}))

        # jstr = {'result':1}
        # return HttpResponse(jstr)

class LoginView(View):
    def get(self,request):

        return render(request,'blog/login.html')

    def post(self,request):

        username = request.POST.get('username')
        password = request.POST.get('passwd')
        uu = {}
        try:
            user = auth.authenticate(username=username, password=password)
            #user = User.objects.filter(username=username)

            if(user and user.is_active == 1):
                auth.login(request,user)
                #if(user_pass):
                result = 1
                userid = user[0].id
                last_login = user[0].last_login
                is_superuser = user[0].is_superuser
                first_name = user[0].first_name
                last_name = user[0].last_name
                email = user[0].email
                uu = {'res':result, 'id':userid,'username': username ,'last_login':last_login,'is_superuser':is_superuser
                          , 'first_name':first_name,'last_name':last_name,'email':email }
                return HttpResponseRedirect('blog/index.html')

        except Exception, e:
            print e
            return HttpResponseRedirect("blog/login.html")



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