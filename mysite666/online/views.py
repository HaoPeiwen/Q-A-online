#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
from django import forms
from models import User


#表单
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    person_choices =(
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
    )
    person =forms.ChoiceField(label='身份',choices=person_choices)
#注册
def regist(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            #获得表单数据
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            person = uf.cleaned_data['person']
            #添加到数据库
            User.objects.create(username= username,password=password,person=person)
            response =  HttpResponseRedirect('/online/turnout/')
            response.set_cookie('username',username,3600)
            response.set_cookie('person',person,3600)
            return response

    else:
        uf = UserForm()
    return render_to_response('regist.html',{'uf':uf}, context_instance=RequestContext(req))

#登陆
def login(req):
    if req.method == 'POST':
        uf = UserForm(req.POST)
        if uf.is_valid():
            #获取表单用户密码
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            person = uf.cleaned_data['person']
            #person = person.object.get(person=uf.cleaned_data['person'])

            #获取的表单数据与数据库进行比较
            user = User.objects.filter(username__exact = username,password__exact = password,person__exact=person)
            if user:
                #比较成功，跳转index
                response = HttpResponseRedirect('/online/index/')
                #将username写入浏览器cookie,失效时间为3600
                response.set_cookie('username',username,3600)
                response.set_cookie('person',person,3600)
                return response
            else:
                #比较失败，还在login
                return HttpResponseRedirect('/online/login/')
    else:
        uf = UserForm()
    return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(req))

#登陆成功
def index(req):
    username = req.COOKIES.get('username','')
    person = req.COOKIES.get('person','')
    dic = {'username':username,'person':person}
    return render_to_response('index.html',dic)


#退出
def logout(req):
    response = HttpResponse('logout !!')
    #清理cookie里保存username
    response.delete_cookie('username')
    return response

def turnout(req):
    username = req.COOKIES.get('username','')
    person = req.COOKIES.get('person','')
    dic = {'username':username,'person':person}
    return render_to_response('turnout.html',dic)

def home(req):
    #return HttpResponseRedirect('/online/home/')
    #这句话没什么卵用，完全仿照以前的形式
    username = req.COOKIES.get('username','')
    return render_to_response('home.html',{'username':username})
