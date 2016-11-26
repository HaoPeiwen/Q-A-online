from models import Category
from django.db.models import Count


class CategoryMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(CategoryMixin, self).get_context_data(*args, **kwargs)
        context['category_list'] = Category.objects.annotate(question_num=Count('question')).order_by('name')
        return context
