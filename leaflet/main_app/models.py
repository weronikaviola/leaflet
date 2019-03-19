from django.db import models
from django.urls import reverse
from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=800)
    date = models.DateTimeField(default=timezone.now)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=200)
    def __str__(self):
        return f'{self.name} by {self.admin.name}'
    def get_absolute_url(self):
        return reverse('add_photo', kwargs={'kind': 'event', 'key': self.id})

class Posting(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=800)
    date = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse('add_photo', kwargs={'kind': 'posting', 'key': self.id})

class Alert(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=800)
    date = models.DateField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    def get_absolute_url(self):
        return reverse('alerts_details', kwargs={'pk': self.id})

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)
    profile_pic = models.CharField(max_length=200, default = 'https://i.imgur.com/1WGonoD.png')
    zip_code = models.IntegerField(default=00000)
    def __str__(self):
        return f'profile: {self.user.first_name}'
    def get_absolute_url(self):
        return reverse('add_photo', kwargs={'kind': 'profile', 'key': self.id})

class Photo(models.Model):
    url = models.CharField(max_length=200)
    event = models.ForeignKey(Event, blank=True, null=True, on_delete=models.CASCADE)
    posting = models.ForeignKey(Posting, blank=True, null=True, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return f"Photo url {self.url}"
    def get_absolute_url(self):
        return reverse('main')
