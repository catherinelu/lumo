from apiclient.discovery import build
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from lumoapp import hue
from oauth2client.django_orm import Storage
from gcal import models as gcal_models
import httplib2
import time

# use default calendar Id
PRIMARY_ID = 'primary'

# use a dummy user in this project
DUMMY_USERNAME = 'corgi'
try:
  dummy_user = User.objects.get(username=DUMMY_USERNAME)
except ObjectDoesNotExist:
  dummy_user = User.objects.create_user(username=DUMMY_USERNAME, password=DUMMY_USERNAME)
  dummy_user.save()


class Command(BaseCommand):
  args = 'none'
  helps = 'try to schedule lights'

  def handle(self, *args, **options):
    user = dummy_user
    events = gcal_models.Event.objects.filter(notified=False, should_notify=False, user=user)

    self.update_events_in_db()

    for event in events:
      # Get the start time as a time struct
      time_zone_start_index = event.start_time.rfind('-')
      start_time_str = event.start_time[:time_zone_start_index]
      start_time = time.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S')

      cur_time = time.localtime()
      min_to_event = (time.mktime(start_time) - time.mktime(cur_time)) / 60

      print abs(event.reminder_time - min_to_event)

      if abs(event.reminder_time - min_to_event) <= 1:
        event.should_notify = True
        event.save()


  def update_events_in_db(self):
    user = dummy_user

    storage = Storage(gcal_models.CredentialsModel, 'id', user, 'credential')
    credential = storage.get()

    # build service for google calendar api
    service = self.build_service(credential)
    cal_lists = self.retrieve_calendar_list(service)
    events = self.retrieve_events_from_calendar(service, PRIMARY_ID)

    # save events to model
    for evt in events:
      start_time = evt['start']['dateTime']
      end_time = evt['end']['dateTime']
      location = evt['location'] if 'location' in evt else ""
      description = evt['summary']

      # See if an event of the same time, description, and user exists. If not,
      # add it into the database
      event = gcal_models.Event.objects.filter(start_time=start_time, user=user, description=description)
      if event.count() == 0: 
        # add the other self defined ones
        reminder_time = 0
        if (not evt['reminders']['useDefault']) and ('overrides' in evt['reminders']):
          for rem in evt['reminders']['overrides']:
            reminder_time = max(reminder_time, int(rem['minutes']))
          evt_entry = gcal_models.Event.objects.create_reminder(user, start_time, end_time, 
            reminder_time, location, description)
        else:
          # add the default reminder
          reminder_time = 30
          evt_entry = gcal_models.Event.objects.create_reminder(user,
            start_time, end_time, reminder_time, location, description)
        evt_entry.save()


  def build_service(self, credential):
    http = httplib2.Http()
    http = credential.authorize(http)
    service = build("calendar", "v3", http=http)
    return service


  # retrieve a list of calendar_id from the service
  def retrieve_calendar_list(self, service):
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
  def retrieve_events_from_calendar(self, service, calendar_id):
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


