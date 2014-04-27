from datetime import datetime, timedelta
import pytz
from django.shortcuts import render
from django import http
from django.core.management import call_command
from django.core.urlresolvers import reverse
# django authentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from gcal import models as gcal_models
from lumoapp import models as lumo_models
import json
from lumoproject import settings
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage
import os, logging, httplib2
import pytz
import time

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '../gcal/client_secrets.json')

FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
  scope=[
      'https://www.googleapis.com/auth/calendar',
      'https://www.googleapis.com/auth/calendar.readonly',
    ],
    # change it to production website once deployed
    redirect_uri='http://localhost:8000/oauth2callback'
    # redirect_uri='http://192.168.1.159:8000/oauth2callback'
    # redirect_uri='./gcal/oauth2callback'
)

# use a dummy user in this project
DUMMY_USERNAME = 'corgi'
try:
  dummy_user = User.objects.get(username=DUMMY_USERNAME)
except ObjectDoesNotExist:
  dummy_user = User.objects.create_user(username=DUMMY_USERNAME, password=DUMMY_USERNAME)
  dummy_user.save()


def get_google_authentication(request, credential):
  user = dummy_user

  if credential is None or credential.invalid == True:
    FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   user)
    authorize_url = FLOW.step1_get_authorize_url()
    print authorize_url
    return http.HttpResponseRedirect(authorize_url)
  elif not request.user.is_authenticated():
    # authenticate user in django
    user = authenticate(username=DUMMY_USERNAME, password=DUMMY_USERNAME)
    login(request, user)

  return http.HttpResponseRedirect(reverse('events'))


def auth_return(request):
  # use dummy_user
  user = dummy_user

  if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'],
                                user):
    return  http.HttpResponseBadRequest()
  credential = FLOW.step2_exchange(request.REQUEST)
  storage = Storage(gcal_models.CredentialsModel, 'id', user, 'credential')
  storage.put(credential)
  return http.HttpResponseRedirect('/')


def events(request):
  # use dummy_user
  user = dummy_user
  storage = Storage(gcal_models.CredentialsModel, 'id', user, 'credential')
  credential = storage.get()
  if credential is None or credential.invalid == True or not request.user.is_authenticated():
    return get_google_authentication(request, credential)

  all_entries = sorted(gcal_models.Event.objects.all(), key=lambda x: x.start_time)

  call_command('schedule_lights', '')
  # preprocessing the events data for later rendering at html

  events_to_return = []

  for entry in all_entries:
    # for the end timing data
    time_zone_end_index = entry.end_time.rfind('-')
    end_time_str = entry.end_time[:time_zone_end_index]
    end_time = time.strptime(end_time_str, '%Y-%m-%dT%H:%M:%S')

    # if the event is already over, don't show it
    cur_time = time.localtime()
    if time.mktime(cur_time) - time.mktime(end_time) > 0:
      continue

    parsed_time = {'year': end_time[0], 'month': numToMonth(end_time[1]), 'date': end_time[2],
               'hour': end_time[3], 'minute': end_time[4], 'suffix': 'am' }

    if parsed_time['hour'] > 12:
      parsed_time['hour'] -= 12
      parsed_time['suffix'] = 'pm'

    if parsed_time['hour'] == 12:
      parsed_time['suffix'] = 'pm'

    if len(str(parsed_time['minute'])) < 2:
      parsed_time['minute'] = '0' + str(parsed_time['minute'])

    entry.end_time = parsed_time

    # for the start timing data
    time_zone_start_index = entry.start_time.rfind('-')
    start_time_str = entry.start_time[:time_zone_start_index]
    start_time = time.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S')
    
    parsed_time = {'year': start_time[0], 'month': numToMonth(start_time[1]), 'date': start_time[2],
               'hour': start_time[3], 'minute': start_time[4], 'suffix': 'am' }

    if parsed_time['hour'] > 12:
      parsed_time['hour'] -= 12
      parsed_time['suffix'] = 'pm'

    if parsed_time['hour'] == 12:
      parsed_time['suffix'] = 'pm'

    if len(str(parsed_time['minute'])) < 2:
      parsed_time['minute'] = '0' + str(parsed_time['minute'])

    entry.start_time = parsed_time
    events_to_return.append(entry)

  return render(request, 'events.html', {'events': events_to_return})


def numToMonth(num):
  month = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  return month[num];


def check_for_notifications(request):
  start_events = gcal_models.Event.objects.filter(should_notify=True, notified=False
    ).order_by('start_time')
  if start_events.count() > 0:
    return http.HttpResponse(json.dumps({'id': start_events[0].id, 'is_end': False}), mimetype='application/json')

  end_events = gcal_models.Event.objects.filter(end_time_should_notify=True,
    end_time_notified=False, remind_end_time=True)
  if end_events.count() > 0:
    return http.HttpResponse(json.dumps({'id': end_events[0].id, 'is_end': True}), mimetype='application/json')

  return http.HttpResponse(None, mimetype='application/json')


def check_for_alarms(request):
  alarms = lumo_models.AlarmEvent.objects.filter(should_notify=True, notified=False
    ).order_by('alarm_time')
  if alarms.count() > 0:
    alarm = alarms[0]
    pst_time = alarm.alarm_time - timedelta(hours=7)
    time_str = '%d:%d' % (pst_time.hour % 12, pst_time.minute)
    time_str += ' AM' if pst_time.hour < 12 else ' PM'
    return http.HttpResponse(json.dumps({'time': time_str, 'id': alarm.id}), mimetype='application/json')
  else:
    return http.HttpResponse(None, mimetype='application/json')


def start_notification_occurred(request, notification_id):
  event = gcal_models.Event.objects.get(pk=notification_id)
  event.notified = True
  event.save()
  return http.HttpResponse(200)


def end_notification_occurred(request, notification_id):
  event = gcal_models.Event.objects.get(pk=notification_id)
  event.end_time_notified = True
  event.save()
  return http.HttpResponse(200)  


def alarm_occurred(request, alarm_id):
  alarm = lumo_models.AlarmEvent.objects.get(pk=alarm_id)
  alarm.notified = True
  alarm.save()
  return http.HttpResponse(200)


def save_alarm(request, hour, minutes):
  hour = int(hour)
  minutes = int(minutes)
  pst_timezone = pytz.timezone('US/Pacific')
  datetime_to_save = pst_timezone.localize(datetime.today())

  # if time already passed for today, then get tomorrow
  if datetime_to_save.hour > hour or datetime_to_save.hour == hour and datetime_to_save.minute > minutes:
    datetime_to_save = datetime_to_save + timedelta(days=1)

  datetime_to_save = datetime_to_save.replace(hour=hour, minute=minutes)

  alarm_event = lumo_models.AlarmEvent(user=dummy_user, alarm_time=datetime_to_save)
  alarm_event.save()

  return http.HttpResponse(200)


def save_dim(request, minutes_to_dim):
  pst_timezone = pytz.timezone('US/Pacific')
  bed_time = pst_timezone.localize(datetime.today())
  dim_event = lumo_models.BedEvent(user=dummy_user, bed_time=bed_time,
    dim_time=minutes_to_dim)
  return http.HttpResponse(200)


def set_end_event_reminder(request, event_id):
  event = gcal_models.Event.objects.get(pk=event_id)
  event.remind_end_time = True
  event.save()
  return http.HttpResponse(200)


def cancel_end_event_reminder(request, event_id):
  event = gcal_models.Event.objects.get(pk=event_id)
  event.remind_end_time = False
  event.save()
  return http.HttpResponse(200)

