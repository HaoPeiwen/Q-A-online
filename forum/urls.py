from django.conf.urls import url
from forum import views

urlpatterns = [
    url('^category/add/$', views.CategoryCreateView.as_view(), name='category-add'),
    url('^category/list/$', views.CategoryListView.as_view(), name='category-list'),
    url('^category/(?P<pk>[0-9]+)/update/$', views.CategoryUpdateView.as_view(), name='category-update'),
    url('^category/(?P<pk>[0-9]+)/delete/$', views.CategoryDeleteView.as_view(), name='category-delete'),
    url('^category/(?P<pk>[0-9]+)/$', views.CategoryQuestionListView.as_view(), name='category-question-list'),

    url('^question/add/$', views.QuestionCreateView.as_view(), name='question-add'),
    url('^question/(?P<pk>[0-9]+)/detail/$', views.QuestionDetailView.as_view(), name='question-detail'),
    url('^question/(?P<pk>[0-9]+)/answer/$', views.AnswerCreateView.as_view(), name='answer-add'),
    url('^question/(?P<pk>[0-9]+)/reply/$', views.ReplyCreateView.as_view(), name='reply-add'),
    url('^question/list/$', views.QuestionListView.as_view(), name='question-list'),
    url('^question/(?P<pk>[0-9]+)/delete/$', views.QuestionDeleteView.as_view(), name='question-delete'),
    url('^question/user/(?P<pk>[0-9]+)/list/$', views.PersonalQuestionListView.as_view(), name='personal-question'),
    url('^answer/user/(?P<pk>[0-9]+)/list/$', views.PersonalAnswerListView.as_view(), name='personal-answer'),
    url('^question/search/$', views.QuestionSearchView.as_view(), name='question-search'),
    url('^question/inviting/(?P<pk>[0-9]+)/list/$', views.PersonalInvitingListView.as_view(), name='personal-inviting'),
    url('^question/reply/(?P<pk>[0-9]+)/list/$', views.PersonalReplyListView.as_view(), name='personal-reply')
]
