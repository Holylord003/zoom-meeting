from django.urls import path

from . import views

app_name = 'meeting_invites'

urlpatterns = [
    path('', views.schedule_meeting, name='schedule_meeting'),
]
