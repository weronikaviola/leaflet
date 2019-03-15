from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('main/', views.main, name='main'),
    path('events/', views.EventsList.as_view(), name='events_index'),
    path('events/create/', views.EventCreate.as_view(), name='events_create'),
    path('events/<int:pk>/details/', views.EventDetail.as_view(), name='events_details'),
    path('events/<int:pk>/update/', views.EventUpdate.as_view(), name='events_update'),
    path('events/<int:pk>/delete/', views.EventDelete.as_view(), name='events_delete'),
    path('postings/', views.PostingList.as_view(), name='postings_index'),
    path('postings/create/', views.PostingCreate.as_view(), name='postings_create'),
    path('postings/<int:pk>/', views.PostingDetail.as_view(), name='postings_details'),
    path('postings/<int:pk>/update/', views.PostingUpdate.as_view(), name='postings_update'),
    path('postings/<int:pk>/delete/', views.PostingDelete.as_view(), name='postings_delete'),
    path('alerts/', views.AlertList.as_view(), name='alerts_index'),
    path('alerts/create/', views.AlertCreate.as_view(), name='alerts_create'),
    path('alerts/<int:pk>/', views.AlertDetail.as_view(), name='alerts_details'),
    path('alerts/<int:pk>/update/', views.AlertUpdate.as_view(), name='alerts_update'),
    path('alerts/<int:pk>/delete/', views.AlertDelete.as_view(), name='alerts_delete'),
    path('settings/<int:user_id>', views.account_settings, name='account_settings'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', views.signup, name='signup'),
]