#coding=utf-8
from django.shortcuts import render
from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from account.models import User

#定义表单模型
class UserForm(forms.Form):
    username = forms.CharField(label='用户名：',max_length=100)
    password = forms.CharField(label='密码：',widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮件：')

#注册
def register(request):
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单信息
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            email = uf.cleaned_data['email']
            #将表单写入数据库
            user = User()
            user.username = username
            user.password = password
            user.email = email
            user.save()
            #返回注册成功页面
            return render_to_response('success_register.html',{'username':username})
    else:
        uf = UserForm()
    return render_to_response('register.html',{'uf':uf})
#登录
def login(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            #获取的表单数据与数据库进行比较
            user = User.objects.filter(username__exact = username,password__exact = password)
            if user:
                return render_to_response('success_login.html',{'username':username})
            else:
                return HttpResponseRedirect('')
    else:
        uf = UserForm()
    return render_to_response('login.html',{'uf':uf})