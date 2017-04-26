# -*- coding:utf-8 -*-
from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名')
    email = forms.EmailField(label='email')
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2= forms.CharField(label='Confirm', widget=forms.PasswordInput)
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
