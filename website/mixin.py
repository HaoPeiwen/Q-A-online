from announcement.mixin import LeastAnnouncementMixin
from authentication.mixin import UserMixin
from forum.mixin import CategoryMixin


class FrontMixin(LeastAnnouncementMixin, UserMixin, CategoryMixin):
    def get_context_data(self, *args, **kwargs):
        return super(FrontMixin, self).get_context_data(*args, **kwargs)
