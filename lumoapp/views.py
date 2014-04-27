from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
# django authentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from gcal import models as gcal_models
from hue import Hue
from oauth2client.client import flow_from_clientsecrets
from oauth2client.django_orm import Storage
import os, logging, httplib2
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
    redirect_uri='http://localhost:8000/gcal/oauth2callback'
    # redirect_uri='./gcal/oauth2callback'
)

# use a dummy user in this project
DUMMY_USERNAME = 'corgi'
try:
  dummy_user = User.objects.get(username=DUMMY_USERNAME)
except ObjectDoesNotExist:
  dummy_user = User.objects.create_user(username=DUMMY_USERNAME, password=DUMMY_USERNAME)
  dummy_user.save()


def get_google_authentication(request):
  # use dummy_user
  user = dummy_user

  storage = Storage(gcal_models.CredentialsModel, 'id', user, 'credential')
  credential = storage.get()

  if credential is None or credential.invalid == True:
    FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   user)
    authorize_url = FLOW.step1_get_authorize_url()
    return HttpResponseRedirect(authorize_url)
  else:
    # authenticate user in django
    user = authenticate(username=DUMMY_USERNAME, password=DUMMY_USERNAME)
    login(request, user)

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


def events(request):
  if not request.user.is_authenticated():
    get_google_authentication(request)

  all_entries = sorted(gcal_models.Event.objects.all(), key=lambda x: x.start_time)

  events = []
  # preprocessing the events data for later rendering at html
  for entry in all_entries:
    # for the timing data
    time_zone_start_index = entry.start_time.rfind('-')
    start_time_str = entry.start_time[:time_zone_start_index]
    start_time = time.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S')
    
    parsed_time = {'year': start_time[0], 'month': numToMonth(start_time[1]), 'date': start_time[2],
               'hour': start_time[3], 'minute': start_time[4], 'suffix': 'am' }

    if parsed_time['hour'] > 12:
      parsed_time['hour'] -= 12
      parsed_time['suffix'] = 'pm'

    if len(str(parsed_time['minute'])) < 2:
      parsed_time['minute'] = '0' + str(parsed_time['minute'])

    entry.start_time = parsed_time

  return render(request, 'events.html', {'events': all_entries})


def numToMonth(num):
  month = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  return month[num];
