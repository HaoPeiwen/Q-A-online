from forum.models import Question


class UserMixin(object):
    def get_context_data(self, **kwargs):
        context = super(UserMixin, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['myuser'] = self.request.user.myuser
            context['inviteing_number'] = Question.objects.filter(inviting_person=self.request.user.myuser).count()
        return context
