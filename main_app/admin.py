from django.contrib import admin

from .models import Profile, Photo, Event, Posting, Alert


admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(Photo)
admin.site.register(Posting)
admin.site.register(Alert)
