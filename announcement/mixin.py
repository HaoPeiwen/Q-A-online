from models import Announcement


class LeastAnnouncementMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(LeastAnnouncementMixin, self).get_context_data(*args, **kwargs)
        if Announcement.objects.count() > 0:
            context['announcement'] = Announcement.objects.all()[0]
        else:
            pass
        return context
