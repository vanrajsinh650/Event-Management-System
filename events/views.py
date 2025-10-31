"""
Views for event-related endpoints.
"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Event, RSVP, Review
from .serializers import EventSerializer, RSVPSerializer, ReviewSerializer
from .permissions import IsOrganizerOrReadOnly


class EventListCreateView(generics.ListCreateAPIView):
    """List all public events or create a new event."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['location', 'is_public']
    search_fields = ['title', 'description']
    ordering_fields = ['start_time', 'created_at']
    ordering = ['-start_time']
    
    def perform_create(self, serializer):
        """Create event with default user as organizer."""
        # Use first user (or create if needed)
        try:
            user = User.objects.first()
            if not user:
                user = User.objects.create_user(username='admin', password='admin')
        except:
            user = User.objects.create_user(username='default_organizer', password='pass123')
        serializer.save(organizer=user)


class EventDetailView(generics.RetrieveAPIView):
    """Retrieve event details."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


class EventUpdateView(generics.UpdateAPIView):
    """Update an event."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


class EventDeleteView(generics.DestroyAPIView):
    """Delete an event."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


class RSVPCreateView(generics.CreateAPIView):
    """Create an RSVP for an event."""
    serializer_class = RSVPSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, event_id):
        """Create RSVP for event."""
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get first user or create
        user = User.objects.first()
        if not user:
            user = User.objects.create_user(username='test_user', password='pass123')
        
        if RSVP.objects.filter(event=event, user=user).exists():
            return Response(
                {'error': 'Already RSVP\'d'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, event=event)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RSVPUpdateView(generics.UpdateAPIView):
    """Update RSVP status."""
    serializer_class = RSVPSerializer
    permission_classes = [AllowAny]
    http_method_names = ['patch']
    
    def patch(self, request, event_id, user_id):
        """Update RSVP status."""
        try:
            rsvp = RSVP.objects.get(event_id=event_id, user_id=user_id)
        except RSVP.DoesNotExist:
            return Response({'error': 'RSVP not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(rsvp, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)


class ReviewListCreateView(generics.ListCreateAPIView):
    """List reviews for an event or create a new review."""
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        """Get all reviews for the specified event."""
        event_id = self.kwargs.get('event_id')
        return Review.objects.filter(event_id=event_id)
    
    def post(self, request, event_id):
        """Create review for event."""
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get first user or create
        user = User.objects.first()
        if not user:
            user = User.objects.create_user(username='test_reviewer', password='pass123')
        
        if Review.objects.filter(event=event, user=user).exists():
            return Response(
                {'error': 'Already reviewed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, event=event)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
