from django.core.urlresolvers import reverse_lazy
from utils.mixin import AjaxableResponseMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from announcement.models import Announcement
from django.http import JsonResponse
from django.contrib.auth.mixins import UserPassesTestMixin


class AnnouncementCreateView(AjaxableResponseMixin, UserPassesTestMixin, CreateView):
    model = Announcement
    fields = ['content']
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('announcement-list')

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super(AnnouncementCreateView, self).get_context_data(**kwargs)
        context['active_page'] = 'announcement-add'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(AnnouncementCreateView, self).form_valid(form)


class AnnouncementListView(UserPassesTestMixin, ListView):
    model = Announcement
    context_object_name = 'announcement_list'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super(AnnouncementListView, self).get_context_data(**kwargs)
        context['active_page'] = 'announcement-list'
        return context


class AnnouncementUpdateView(AjaxableResponseMixin, UserPassesTestMixin, UpdateView):
    model = Announcement
    context_object_name = 'announcement'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('announcement-list')
    fields = ['content']

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super(AnnouncementUpdateView, self).get_context_data(**kwargs)
        context['active_page'] = 'announcement-update'
        return context


class AnnouncementDeleteView(AjaxableResponseMixin, UserPassesTestMixin, DeleteView):
    model = Announcement
    success_url = reverse_lazy('announcement-list')

    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, *args, **kwargs):
        super(AnnouncementDeleteView, self).post(request, *args, **kwargs)
        return JsonResponse({'state': 'success'})
