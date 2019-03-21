from django.contrib import admin

from .models import Profile, Photo, Event


admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(Photo)
