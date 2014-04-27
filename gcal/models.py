from django.db import models
from django.contrib.auth.models import User
from oauth2client.django_orm import FlowField
from oauth2client.django_orm import CredentialsField

class FlowModel(models.Model):
  id = models.ForeignKey(User, primary_key=True)
  flow = FlowField()

class CredentialsModel(models.Model):
  id = models.ForeignKey(User, primary_key=True)
  credential = CredentialsField()

# create Manager for the model
class EventManager(models.Manager):
  def create_reminder(self, user, start_time, end_time, reminder_time=30, location="", description=""):
    event = self.create(user=user, start_time=start_time, end_time=end_time, reminder_time=reminder_time, location=location, description=description)
    # do something with the reminder
    return event

class Event(models.Model):
  user = models.ForeignKey(User)
  start_time = models.CharField(max_length=200)
  end_time = models.CharField(max_length=200)
  reminder_time = models.IntegerField(default=30)
  location = models.CharField(max_length=200)
  description = models.CharField(max_length=200)
  notified = models.BooleanField(default=False)  # Lights notified user
  should_notify = models.BooleanField(default=False)  # Lights should notify user, but haven't yet
  remind_end_time = models.BooleanField(default=False)
  end_time_notified = models.BooleanField(default=False)
  end_time_should_notify = models.BooleanField(default=False)

  objects = EventManager()

  def __unicode__(self):  # Python 3: def __str__(self):
    return self.description