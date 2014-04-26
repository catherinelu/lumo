from django.core.management.base import BaseCommand
from gcal import models as gcal_models
from lumoapp import hue
import time

class Command(BaseCommand):
    args = 'none'
    helps = 'try to schedule lights'

    def handle(self, *args, **options):
        events = gcal_models.Event.objects.all()

        h = hue.Hue()
        h.get_state()
        light = h.lights.get('l1')

        for event in events:
            # Get the start time as a time struct
            time_zone_start_index = event.start_time.rfind('-')
            start_time_str = event.start_time[:time_zone_start_index]
            start_time = time.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S')

            cur_time = time.localtime()
            min_to_event = (time.mktime(start_time) - time.mktime(cur_time)) / 60

            if abs(event.reminder_time - min_to_event) <= 5:
                light.on()
                light.toggle()
