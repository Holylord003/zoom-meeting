from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.html import strip_tags

from .forms import MeetingInviteForm


def schedule_meeting(request):
    if request.method == 'POST':
        form = MeetingInviteForm(request.POST)
        if form.is_valid():
            try:
                _send_meeting_invite(form.cleaned_data)
            except (SMTPException, OSError, ValueError) as exc:
                messages.error(
                    request,
                    'We could not send the invitation. Please verify your email settings and try again.',
                )
                if settings.DEBUG:
                    messages.error(request, str(exc))
            else:
                messages.success(
                    request,
                    f'Invitation sent successfully to {form.cleaned_data["recipient_email"]}.',
                )
                return redirect('meeting_invites:schedule_meeting')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MeetingInviteForm()

    return render(request, 'schedule_meeting.html', {'form': form})


def _send_meeting_invite(cleaned_data):
    meeting_dt = cleaned_data['meeting_time']
    if timezone.is_naive(meeting_dt):
        meeting_dt = timezone.make_aware(meeting_dt, timezone.get_current_timezone())
    local_dt = timezone.localtime(meeting_dt)

    meeting_date_display = date_format(local_dt, 'l, F j, Y')
    meeting_time_display = date_format(local_dt, 'g:i A')

    recipient_name = (cleaned_data.get('recipient_name') or '').strip()
    sender_name = (cleaned_data.get('sender_name') or '').strip()
    meeting_link = (cleaned_data.get('meeting_link') or '').strip()

    context = {
        'recipient_name': recipient_name,
        'sender_name': sender_name,
        'meeting_link': meeting_link,
        'duration': cleaned_data['duration'],
        'platform': cleaned_data['platform'],
        'meeting_date': meeting_date_display,
        'meeting_time': meeting_time_display,
    }

    html_body = render_to_string('emails/meeting_invite.html', context)
    plain_body = strip_tags(html_body)
    plain_body = '\n'.join(line.strip() for line in plain_body.splitlines() if line.strip())

    subject = (
        f'Zoom meeting invitation from {sender_name}'
        if sender_name
        else 'Zoom meeting invitation'
    )

    message = EmailMultiAlternatives(
        subject=subject,
        body=plain_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[cleaned_data['recipient_email']],
    )
    message.attach_alternative(html_body, 'text/html')
    message.send(fail_silently=False)
