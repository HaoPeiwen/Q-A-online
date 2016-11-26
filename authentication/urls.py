from django.conf.urls import url
from authentication import views

urlpatterns = [
    url(r'user/signup/$', views.SignupView.as_view(), name='user-signup'),
    url(r'user/logout/$', views.LogoutView.as_view(), name='user-logout'),
    url(r'user/login/$', views.LoginView.as_view(), name='user-login'),
    url(r'user/list/$', views.UserListView.as_view(), name='myuser-list'),
    url(r'user/photo/(?P<pk>[0-9]+)/update/$', views.UserPhotoChangeView.as_view(), name='user-change-photo')
]
