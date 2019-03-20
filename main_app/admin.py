from django.contrib import admin

from .models import Event
from .models import Profile, Photo


admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(Photo)
