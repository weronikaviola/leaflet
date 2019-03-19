from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, QueryDict
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import UserForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from main_app import views


import uuid
import boto3
from .models import Event, Posting, Alert, Profile, Photo

S3_BASE_URL='https://s3-us-west-1.amazonaws.com/'
BUCKET='recordcollector'


def home(request):
    if (request.user.id == None):
        return render(request, 'main_app/landing.html')
    else: 
        return redirect('main')

@login_required
def main(request):
    return render(request, 'main_app/index.html')

##### events #####
class EventsList(LoginRequiredMixin, ListView):
    model = Event

class EventDetail(LoginRequiredMixin, DetailView):
    model = Event

class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['name', 'date', 'description', 'location']
    def form_valid(self, form):
        form.instance.admin = self.request.user
        return super().form_valid(form)

class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    fields = [ 'name', 'date', 'description', 'location']

class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = '/events/'

######################postings###########################
class PostingList(LoginRequiredMixin, ListView):
    model = Posting

class PostingDetail(LoginRequiredMixin, DetailView):
    model = Posting

class PostingCreate(LoginRequiredMixin, CreateView):
    model = Posting
    fields = ['title', 'description', 'date']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostingUpdate(LoginRequiredMixin, UpdateView):
    model = Posting
    fields = ['title', 'description', 'date']

class PostingDelete(LoginRequiredMixin, DeleteView):
    model = Posting
    success_url = '/postings/'

################### alerts #########################
class AlertList(LoginRequiredMixin, ListView):
    model = Alert

class AlertDetail(LoginRequiredMixin, DetailView):
    model = Alert

class AlertCreate(LoginRequiredMixin, CreateView):
    model = Alert
    fields = ['title', 'description', 'date']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    success_url = '/alerts/'

class AlertUpdate(LoginRequiredMixin, UpdateView):
    model = Alert
    fields = '__all__'

class AlertDelete(LoginRequiredMixin, DeleteView):
    model = Alert
    success_url = '/alerts/'
###################### accounts ##################
class ProfileCreate(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ['nickname', 'zip_code']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['nickname', 'zip_code']
    success_url = '/main'

# @login_required
# def account_settings(request, user_id):
#     try:
#         profile = Profile.objects.get(user=user_id)
#         return ProfileUpdate.as_view()(request, pk=profile.id)
#     except ObjectDoesNotExist:
#         return ProfileCreate.as_view()(request, pk=profile.id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile_create')
        else:
            error_message = 'Invalid credentials - try again'
    form = UserForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def add_photo(request, kind, obj_id):
    skip_url = f'/{kind}/' if (kind == 'events' or kind == 'postings') else '/main/' 
    if request.method =='GET':
        data = {
            'kind': kind,
            'obj_id': obj_id,
            'skip_url': skip_url
        }
        return render(request, 'add_photo.html', data)
    else:
        photo_file = request.FILES.get('photo-file', None)
        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            
            try: 
                s3.upload_fileobj(photo_file, BUCKET, key)
                url = f"{S3_BASE_URL}{BUCKET}/{key}"
                if kind == 'postings':
                    pst = Posting.objects.get(id=obj_id)
                    photo = Photo(url=url, posting=pst)
                elif kind == 'events':
                    evt = Event.objects.get(id=obj_id)
                    photo = Photo(url=url, event=evt)
                elif kind == 'profile':
                    prf = Profile.objects.get(id=obj_id)
                    photo = Photo(url=url, profile=prf)
                photo.save()
            except:
                print('An error ocurred uploading file to S3')
                ##weronika redirct to the kind
        return redirect('main' if kind == 'profile' else f'/{kind}/')