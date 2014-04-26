from django.shortcuts import render
from hue import Hue

def home(request):
    h = Hue()
    h.get_state()
    light = h.lights.get('l1')
    light.on()
    light.bri(255)
    light.off()
    return render(request, 'home.epy')


