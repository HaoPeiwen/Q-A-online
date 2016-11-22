from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite666.views.home', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^online/', include('online.urls')),
)
