# coding=utf-8
from django.contrib.auth import logout, login
from django.shortcuts import render
from django.views.generic import CreateView, RedirectView, FormView, ListView
from django.core.urlresolvers import reverse_lazy
from website.mixin import FrontMixin
from django.contrib.auth.models import User
from authentication.models import MyUser
from forms import LoginForm
from django.contrib.auth.mixins import UserPassesTestMixin


class SignupView(FrontMixin, CreateView):
    model = MyUser
    fields = ['nickname', 'identity']   #在此处删除了‘photo’，使注册时头像上传不是必须项
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('user-login')

    def form_valid(self, form):
        username = form.data.get('username', '')
        password = form.data.get('password', '')
        email = form.data.get('email', '')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        form.instance.user = user
        return super(SignupView, self).form_valid(form)

    def form_invalid(self, form):
        print form.errors
        return render(self.request, 'utils/error_page.html', {'message': form.errors})


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
        return render(self.request, 'utils/error_page.html', {'message': msg})


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
