from django.shortcuts import render
from hue import Hue

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

# django authentication
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

import os, logging, httplib2

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

  all_entries = Event.objects.all()
  return render(request, 'events.html')
