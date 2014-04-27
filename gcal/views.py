from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader

# django authentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

import os, logging, httplib2

# import for oauth2
from oauth2client.django_orm import Storage
from oauth2client import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from apiclient.discovery import build

# import from this project
from gcal.models import CredentialsModel, FlowModel
from lumoproject import settings
from gcal.models import Event

# use a dummy user in this project
DUMMY_USERNAME = 'corgi'
try:
  dummy_user = User.objects.get(username=DUMMY_USERNAME)
except ObjectDoesNotExist:
  dummy_user = User.objects.create_user(username=DUMMY_USERNAME, password=DUMMY_USERNAME)
  dummy_user.save()

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
  scope=[
      'https://www.googleapis.com/auth/calendar',
      'https://www.googleapis.com/auth/calendar.readonly',
    ],
    # change it to production website once deployed
    redirect_uri='http://localhost:8000/gcal/oauth2callback'
    # redirect_uri='./gcal/oauth2callback'
)

# use default calendar Id
PRIMARY_ID = "primary"

def google_auth(user):
  FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                 user)
  authorize_url = FLOW.step1_get_authorize_url()
  return HttpResponseRedirect(authorize_url)

# retrieve a list of calendar_id from the service
def retrieve_calendar_list(service):
  calendar_list = []
  # get all calendars, store in calendar_list
  # no need for calendarId
  page_token = None
  while True:
    cur_cal_lists = service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in cur_cal_lists['items']:
      calendar_list.append(calendar_list_entry['id'])
    page_token = cur_cal_lists.get('nextPageToken')
    if not page_token:
      break
  return calendar_list

# retrieve a list of events from the given service and calendar id
def retrieve_events_from_calendar(service, calendar_id):
  events = []
# get all events from primary calendar, store in events
  page_token = None
  while True:
    cur_events = service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
    for event in cur_events['items']:
      events.append(event)
      # print event['summary'], event['start']['dateTime']
    page_token = cur_events.get('nextPageToken')
    if not page_token:
      break
  return events

def build_service(credential):
  http = httplib2.Http()
  http = credential.authorize(http)
  service = build("calendar", "v3", http=http)
  return service

def index(request):
  # use dummy_user
  user = dummy_user

  storage = Storage(CredentialsModel, 'id', user, 'credential')
  credential = storage.get()

  if credential is None or credential.invalid == True:
    return google_auth(user)
  else:
    # authenticate user in django
    user = authenticate(username=DUMMY_USERNAME, password=DUMMY_USERNAME)
    login(request, user)

    # build service for google calendar api
    service = build_service(credential)
    cal_lists = retrieve_calendar_list(service)
    events = retrieve_events_from_calendar(service, PRIMARY_ID)

    # delete old entries for the user
    Event.objects.filter(user=user).delete()
    # save events to model
    for evt in events:
      user_name = user
      start_time = evt['start']['dateTime']
      location = evt['location'] if 'location' in evt else ""
      description = evt['summary']
      
      # add the other self defined ones
      reminder_time = 0
      if (not evt['reminders']['useDefault']) and ('overrides' in evt['reminders']):
        for rem in evt['reminders']['overrides']:
          reminder_time = max(reminder_time, int(rem['minutes']))
        evt_entry = Event.objects.create_reminder(user_name, start_time, reminder_time, location, description)
      else:
        # add the default reminder
        reminder_time = 30
        evt_entry = Event.objects.create_reminder(user_name, start_time, reminder_time, location, description)
      evt_entry.save()

    # queryset = Event.objects.all()
    # sorted_queryset = sorted(queryset, key=lambda x: x.start_time)
    # print([p.start_time for p in sorted_queryset])

    return HttpResponseRedirect(reverse('events'))


def auth_return(request):
  # use dummy_user
  user = dummy_user

  if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'],
                                user):
    return  HttpResponseBadRequest()
  credential = FLOW.step2_exchange(request.REQUEST)
  storage = Storage(CredentialsModel, 'id', user, 'credential')
  storage.put(credential)
  return HttpResponseRedirect("/gcal/")
















