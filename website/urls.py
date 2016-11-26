from django.conf.urls import url
from website import views

urlpatterns = [
    url(r'^dashboard/$', views.DashboardOverviewView.as_view(), name='dashboard'),
    url(r'^$', views.HomepageView.as_view(), name='homepage'),
]
