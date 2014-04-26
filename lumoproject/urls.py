from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lumoproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^gcal/', include('gcal.urls', namespace='gcal')),
    url(r'^admin/', include(admin.site.urls)),
)
