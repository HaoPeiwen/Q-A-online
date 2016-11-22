from django.conf.urls import patterns, url
from online import views

 
urlpatterns = patterns('',
    url(r'^$', views.login, name='login'),
    url(r'^login/$',views.login,name = 'login'),
    url(r'^regist/$',views.regist,name = 'regist'),
    url(r'^index/$',views.index,name = 'index'),
    url(r'^logout/$',views.logout,name = 'logout'),
    url(r'^turnout/$',views.turnout,name = 'turnout'),
    url(r'^home/$',views.home,name = 'home'),
)
