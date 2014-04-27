from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'lumoapp.views.events', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^events$', 'lumoapp.views.events', name='events'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^oauth2callback$', 'lumoapp.views.auth_return', name='auth_return')
)
