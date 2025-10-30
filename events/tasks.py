from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Event
from django.contrib.auth.models import User

@shared_task
def send_rsvp_notification(event_id, user_id, rsvp_status):
    try:
        event = Event.objects.get(id=event_id)
        user = User.objects.get(id=user_id)
        
        subject = f'New RSVP for your event: {event.title}'
        message = f'{user.username} has RSVP\'d to your event "{event.title}" with status: {rsvp_status}.'
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[event.organizer.email],
            fail_silently=False,
        )
        return f'Notification sent for event {event_id}'
    except Exception as e:
        return f'Error: {str(e)}'

@shared_task
def send_review_notification(event_id, user_id, rating):
    try:
        event = Event.objects.get(id=event_id)
        user = User.objects.get(id=user_id)
        
        subject = f'New review for your event: {event.title}'
        message = f'{user.username} has reviewed your event "{event.title}" with {rating}/5 stars.'
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[event.organizer.email],
            fail_silently=False,
        )
        return f'Review notification sent for event {event_id}'
    except Exception as e:
        return f'Error: {str(e)}'