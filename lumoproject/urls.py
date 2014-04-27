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
    url(r'^check-for-dims/$', 'lumoapp.views.check_for_dims'),      
    url(r'^save-alarm/(?P<hour>\d+)/(?P<minutes>\d+)/$', 'lumoapp.views.save_alarm'),  
    url(r'^save-dim/(?P<minutes>\d+)/$', 'lumoapp.views.save_dim'),
    url(r'^start-notification-occurred/(?P<notification_id>\d+)/$',
        'lumoapp.views.start_notification_occurred'),
    url(r'^end-notification-occurred/(?P<notification_id>\d+)/$',
        'lumoapp.views.end_notification_occurred'),
    url(r'^alarm-occurred/(?P<alarm_id>\d+)/$', 'lumoapp.views.alarm_occurred'),
    url(r'^set-end-event-reminder/(?P<event_id>\d+)/$', 'lumoapp.views.set_end_event_reminder'),    
    url(r'^cancel-end-event-reminder/(?P<event_id>\d+)/$', 'lumoapp.views.cancel_end_event_reminder'),    
)
