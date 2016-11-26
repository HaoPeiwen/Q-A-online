from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import UserPassesTestMixin
from forum.models import Question
from website.mixin import FrontMixin
from django.core.urlresolvers import reverse_lazy


class HomepageView(FrontMixin, ListView):
    template_name = 'website/frontend/homepage.html'
    model = Question
    paginate_by = 10
    context_object_name = 'question_list'


class DashboardOverviewView(UserPassesTestMixin, TemplateView):
    login_url = reverse_lazy('user-login')
    template_name = 'website/backend/overview.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super(DashboardOverviewView, self).get_context_data(**kwargs)
        context['active_page'] = 'overview'
        return context
