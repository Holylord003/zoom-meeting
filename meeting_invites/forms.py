from django import forms
from django.utils import timezone


class MeetingInviteForm(forms.Form):
    recipient_name = forms.CharField(
        label='Victim name',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'name'}),
    )
    recipient_email = forms.EmailField(
        label='Victim email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete': 'email'}),
    )
    meeting_time = forms.DateTimeField(
        label='Meeting date & time',
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M',
        ),
        initial=timezone.now(),
        input_formats=[
            '%Y-%m-%dT%H:%M',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M',
        ],
    )
    sender_name = forms.CharField(
        label='Sender name',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'name'}),
    )
    duration = forms.CharField(
        label='Duration',
        max_length=100,
        required=False,
        initial='45',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 45 minutes'}),
    )
    platform = forms.CharField(
        label='Platform',
        max_length=100,
        initial='Zoom',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
