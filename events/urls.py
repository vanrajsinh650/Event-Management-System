"""
URL patterns for event-related endpoints.
"""
from django.urls import path
from .views import (
    EventListCreateView,
    EventDetailView,
    EventUpdateView,
    EventDeleteView,
    RSVPCreateView,
    RSVPUpdateView,
    ReviewListCreateView,
)

urlpatterns = [
    #Event endpoints
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/<int:pk>/update/', EventUpdateView.as_view(), name='event-update'),
    path('events/<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),
    
    #RSVP endpoints
    path('events/<int:event_id>/rsvp/', RSVPCreateView.as_view(), name='rsvp-create'),
    path('events/<int:event_id>/rsvp/<int:user_id>/', RSVPUpdateView.as_view(), name='rsvp-update'),
    
    #Review endpoints
    path('events/<int:event_id>/reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
]
