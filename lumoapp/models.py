from django.db import models
from django.contrib.auth.models import User

class AlarmEvent(models.Model):
  user = models.ForeignKey(User)
  alarm_time = models.DateTimeField()
  notified = models.BooleanField(default=False)
  should_notify = models.BooleanField(default=False)


class BedEvent(models.Model):
  user = models.ForeignKey(User)
  bed_time = models.DateTimeField()
  dim_time = models.IntegerField(default=10)
