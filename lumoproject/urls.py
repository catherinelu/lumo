from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'lumoapp.views.events', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^events$', 'lumoapp.views.events', name='events'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^oauth2callback$', 'lumoapp.views.auth_return', name='auth_return'),
    url(r'^check-for-notifications/$', 'lumoapp.views.check_for_notifications'),    
    url(r'^check-for-alarms/$', 'lumoapp.views.check_for_alarms'),    
    url(r'^notification-occurred/(?P<notification_id>\d+)/$',
        'lumoapp.views.notification_occurred'),
    url(r'^alarm-occurred/(?P<alarm_id>\d+)/$', 'lumoapp.views.alarm_occurred'),
    url(r'^save-alarm/(?P<hour>\d+)/(?P<minutes>\d+)/$', 'lumoapp.views.save_alarm'),    
)
