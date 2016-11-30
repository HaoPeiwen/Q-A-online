from django.core.urlresolvers import reverse_lazy, reverse
from forum.models import Category, Question, Answer
from utils.mixin import AjaxableResponseMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import JsonResponse, Http404
from website.mixin import FrontMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from authentication.models import MyUser


class CategoryCreateView(UserPassesTestMixin, AjaxableResponseMixin, CreateView):
    login_url = reverse_lazy('user-login')
    model = Category
    fields = ['name']
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('category-list')

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['active_page'] = 'category-add'
        return context


class CategoryListView(UserPassesTestMixin, ListView):
    login_url = reverse_lazy('user-login')
    model = Category
    context_object_name = 'category_list'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['active_page'] = 'category-list'
        return context


class CategoryUpdateView(UserPassesTestMixin, AjaxableResponseMixin, UpdateView):
    login_url = reverse_lazy('user-login')
    model = Category
    context_object_name = 'category'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('category-list')
    fields = ['name']

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['active_page'] = 'category-update'
        return context


class CategoryDeleteView(UserPassesTestMixin, AjaxableResponseMixin, DeleteView):
    login_url = reverse_lazy('user-login')
    model = Category
    success_url = reverse_lazy('category-list')

    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, *args, **kwargs):
        super(CategoryDeleteView, self).post(request, *args, **kwargs)
        return JsonResponse({'state': 'success'})


class QuestionCreateView(LoginRequiredMixin, FrontMixin, CreateView):
    login_url = reverse_lazy('user-login')
    model = Question
    template_name_suffix = '_create_form'
    fields = ['title', 'content', 'category', 'inviting_person']

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionCreateView, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['teacher_list'] = MyUser.objects.filter(identity='T').order_by('nickname')
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.show_times = 0
        return super(QuestionCreateView, self).form_valid(form)

    def get_success_url(self):
        questions_list = Question.objects.filter(author=self.request.user).order_by('-publish_time')
        least_question = questions_list[0]
        return reverse('question-detail', kwargs={'pk': least_question.id})


class CategoryQuestionListView(FrontMixin, ListView):
    template_name = 'website/frontend/homepage.html'
    model = Question
    paginate_by = 10
    context_object_name = 'question_list'

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Question.objects.filter(category=category)


class QuestionDetailView(FrontMixin, ListView):
    model = Answer
    template_name = 'forum/question_detail.html'
    paginate_by = 10
    context_object_name = 'answer_list'

    def get_queryset(self):
        question = Question.objects.get(pk=self.kwargs['pk'])
        question.show_times += 1
        question.save()
        return Answer.objects.filter(question=question)

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(*args, **kwargs)
        context['question'] = Question.objects.get(pk=self.kwargs['pk'])
        return context


class AnswerCreateView(LoginRequiredMixin, FrontMixin, CreateView):
    model = Answer
    template_name = 'forum/answer_create_form.html'
    fields = ['content']
    login_url = reverse_lazy('user-login')

    def get_context_data(self, *args, **kwargs):
        context = super(AnswerCreateView, self).get_context_data(*args, **kwargs)
        context['question'] = Question.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('question-detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.question = Question.objects.get(pk=self.kwargs['pk'])
        return super(AnswerCreateView, self).form_valid(form)
    
class ReplyCreateView(LoginRequiredMixin, FrontMixin, CreateView):
    model = Answer
    template_name = 'forum/reply_create_form.html'
    fields = ['content']
    login_url = reverse_lazy('user-login')
    
    def get_context_data(self, *args, **kwargs):
        context = super(ReplyCreateView, self).get_context_data(*args, **kwargs)
        answer=Answer.objects.get(pk=self.kwargs['pk'])
        context['answer'] = Answer.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        answer=Answer.objects.get(pk=self.kwargs['pk'])
        
        return reverse('question-detail', kwargs={'pk': answer.question.pk})

    def form_valid(self, form):
        answer=Answer.objects.get(pk=self.kwargs['pk'])
        question=answer.question
        form.instance.author = self.request.user
        form.instance.question = question
        form.instance.reply_author=answer.author.myuser
        
        return super(ReplyCreateView, self).form_valid(form)



class QuestionListView(UserPassesTestMixin, ListView):
    model = Question
    login_url = reverse_lazy('user-login')
    context_object_name = 'question_list'
    template_name = 'forum/question_list.html'

    def test_func(self):
        return self.request.user.is_staff


class QuestionDeleteView(UserPassesTestMixin, AjaxableResponseMixin, DeleteView):
    login_url = reverse_lazy('user-login')
    model = Question
    success_url = reverse_lazy('question-list')

    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, *args, **kwargs):
        super(QuestionDeleteView, self).post(request, *args, **kwargs)
        return JsonResponse({'state': 'success'})


class PersonalQuestionListView(FrontMixin, ListView):
    paginate_by = 10
    template_name = 'forum/question_weight2.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Question.objects.filter(author_id=self.kwargs['pk'])
    def get_context_data(self, *args, **kwargs):
        context = super(PersonalQuestionListView, self).get_context_data(**kwargs)
        context['theuser']=MyUser.objects.get(pk=self.kwargs['pk'])
        return context

class PersonalAnswerListView(FrontMixin, ListView):
    paginate_by = 10
    template_name = 'forum/answer_weight.html'
    context_object_name = 'question_asked_list'

    def get_queryset(self):
        answers = Answer.objects.filter(author_id=self.kwargs['pk'])
        question_asked_list = list(set([item.question for item in answers]))
        question_asked_list.reverse()
        return  question_asked_list

    def get_context_data(self, *args, **kwargs):
        context = super(PersonalAnswerListView, self).get_context_data(**kwargs)
        context['theuser']=MyUser.objects.get(pk=self.kwargs['pk'])
        return context


class QuestionSearchView(FrontMixin, ListView):
    paginate_by = 10
    template_name = 'website/frontend/homepage.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Question.objects.filter(title__contains=self.request.GET.get('keyword', ''))


class PersonalInvitingListView(FrontMixin, ListView):
    paginate_by = 10
    template_name = 'website/frontend/homepage.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Question.objects.filter(inviting_person=MyUser.objects.get(pk=self.kwargs['pk']))

class PersonalReplyListView(FrontMixin, ListView):
    paginate_by = 10
    template_name = 'forum/reply_weight.html'
    context_object_name = 'reply_list'

    def get_queryset(self):
        return Answer.objects.filter(reply_author=MyUser.objects.get(pk=self.kwargs['pk'])).order_by('-publish_time')
