from django.shortcuts import render
from hue import Hue

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

# django authentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

import os, logging, httplib2
import time

from gcal.models import Event

def home(request):
    h = Hue()
    h.get_state()
    light = h.lights.get('l1')
    light.on()
    light.bri(255)
    light.off()
    return render(request, 'home.epy')

def events(request):
  if not request.user.is_authenticated():
    return HttpResponseRedirect(reverse('gcal:index'))

  all_entries = sorted(Event.objects.all(), key=lambda x: x.start_time)

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

    if parsed_time['hour'] == 12:
      parsed_time['suffix'] = 'pm'

    if len(str(parsed_time['minute'])) < 2:
      parsed_time['minute'] = '0' + str(parsed_time['minute'])

    entry.start_time = parsed_time

  return render(request, 'events.html', {'events': all_entries})

def numToMonth(num):
  month = [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  return month[num];