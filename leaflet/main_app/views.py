from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import UserForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .models import Event, Posting, Alert

def home(request):
    return HttpResponse('home')
def main(request):
    return render(request, 'main_app/index.html')
##### events #####
class EventsList(ListView):
    model = Event
class EventDetail(DetailView):
    model = Event
class EventCreate(CreateView):
    model = Event
    fields = ['date', 'description', 'name', 'location']
    def form_valid(self, form):
        form.instance.admin = self.request.user
        return super().form_valid(form)
class EventUpdate(UpdateView):
    model = Event
    fields = ['date', 'description', 'name', 'location']
class EventDelete(DeleteView):
    model = Event
    success_url = '/events/'
#######postings#######
class PostingList(ListView):
    model = Posting
class PostingDetail(DetailView):
    model = Posting
class PostingCreate(CreateView):
    model = Posting
    fields = ['title', 'description', 'date']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
class PostingUpdate(UpdateView):
    model = Posting
    fields = ['title', 'description', 'date']
class PostingDelete(DeleteView):
    model = Posting
    success_url = '/postings/'
#### alerts #####
class AlertList(ListView):
    model = Alert
class AlertDetail(DetailView):
    model = Alert
class AlertCreate(CreateView):
    model = Alert
    fields = '__all__'
class AlertUpdate(UpdateView):
    model = Alert
    fields = '__all__'
class AlertDelete(DeleteView):
    model = Alert
    success_url = '/alerts/'
###### accounts ######3
def account_settings(request):
    return HttpResponse('settings WILL BE HERE ;)')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid credentials - try again'
    form = UserForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)