from django.db import models

# Create your models here.

import pickle
import base64

from django.contrib import admin
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
  def create_reminder(self, user, start_time, reminder_time=30, location="", description=""):
    event = self.create(user=user, start_time=start_time, reminder_time=reminder_time, location=location, description=description)
    # do something with the reminder
    return event

class Event(models.Model):
  user = models.ForeignKey(User)
  start_time = models.CharField(max_length=200)
  reminder_time = models.IntegerField(default=30)
  location = models.CharField(max_length=200)
  description = models.CharField(max_length=200)

  objects = EventManager()

  def __unicode__(self):  # Python 3: def __str__(self):
    return self.description