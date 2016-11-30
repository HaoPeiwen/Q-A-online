# coding=utf-8
from django.contrib.auth import logout, login
from django.db.models import Count
from django.shortcuts import render
from django.views.generic import CreateView, RedirectView, FormView, ListView, UpdateView
from django.core.urlresolvers import reverse_lazy

from announcement.models import Announcement
from forum.models import Category
from website.mixin import FrontMixin
from django.contrib.auth.models import User
from authentication.models import MyUser
from forms import LoginForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class SignupView(FrontMixin, CreateView):
    model = MyUser
    fields = ['nickname', 'identity', 'photo']
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('user-login')

    def form_valid(self, form):
        username = form.data.get('username', '')
        password = form.data.get('password', '')
        email = form.data.get('email', '')
        if User.objects.filter(username=username):
            return render(self.request, 'utils/error_page.html', {'message': '该用户名已被占用'})
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        form.instance.user = user
        return super(SignupView, self).form_valid(form)

    def form_invalid(self, form):
        print form.errors
        context = {'message': form.errors, 'announcement': Announcement.objects.all()[0],
                   'category_list': Category.objects.annotate(question_num=Count('question')).order_by('name')}
        return render(self.request, 'utils/error_page.html', context)


class LogoutView(RedirectView):
    pattern_name = 'homepage'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)


class LoginView(FrontMixin, FormView):
    template_name = 'authentication/user_login.html'
    success_url = reverse_lazy('homepage')
    form_class = LoginForm

    def form_valid(self, form):
        user = form.login()
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return super(LoginView, self).form_valid(form)
            else:
                return self.response_error_page('你的账户尚未激活')
        else:
            return self.response_error_page('用户名或密码错误')

    def response_error_page(self, msg):
        context = {'message': msg, 'announcement': Announcement.objects.all()[0],
                   'category_list': Category.objects.annotate(question_num=Count('question')).order_by('name')}
        return render(self.request, 'utils/error_page.html', context)


class UserListView(UserPassesTestMixin, ListView):
    login_url = reverse_lazy('user-login')
    model = MyUser
    paginate_by = 30
    context_object_name = 'user_list'
    template_name = 'authentication/user_list.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['active_page'] = 'myuser-list'
        return context


class UserPhotoChangeView(LoginRequiredMixin, FrontMixin, UpdateView):
    login_url = reverse_lazy('user-login')
    success_url = reverse_lazy('homepage')
    template_name = 'authentication/photo_change_form.html'
    fields = ['photo']
    model = MyUser

    def form_valid(self, form):
        if int(self.kwargs['pk']) != self.request.user.myuser.id:
            return self.response_error_page('权限错误')
        return super(UserPhotoChangeView, self).form_valid(form)

    def response_error_page(self, msg):
        return render(self.request, 'utils/error_page.html', {'message': msg, 'myuser': self.request.user.myuser})
