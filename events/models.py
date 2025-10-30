from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_public = models.BooleanField(default=True)  # Added this
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Added this
    
    class Meta:
        ordering = ['-start_time']
    
    def __str__(self):
        return self.title
    
    def clean(self):
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError({'end_time': 'End time must be after start time.'})
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class RSVP(models.Model):
    STATUS_CHOICES = [
        ('Going', 'Going'),
        ('Maybe', 'Maybe'),
        ('Not Going', 'Not Going'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rsvps')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.status}"
    
    def clean(self):
        if self.event.organizer == self.user:
            raise ValidationError({'user': 'Event organizer cannot RSVP to their own event.'})
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
