"""
Views for event-related endpoints.
"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

from .models import Event, RSVP, Review
from .serializers import EventSerializer, RSVPSerializer, ReviewSerializer
from .permissions import IsOrganizerOrReadOnly


class EventListCreateView(generics.ListCreateAPIView):
    """List all public events or create a new event."""
    serializer_class = EventSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['location', 'is_public']
    search_fields = ['title', 'description']
    ordering_fields = ['start_time', 'created_at']
    ordering = ['-start_time']
    
    def get_queryset(self):
        """Return queryset of events based on user access."""
        user = self.request.user
        
        if user.is_authenticated:
            queryset = Event.objects.filter(is_public=True)
            private_events = Event.objects.filter(
                Q(is_public=False) &
                (Q(organizer=user) | Q(rsvps__user=user))
            ).distinct()
            return (queryset | private_events).distinct()
        else:
            return Event.objects.filter(is_public=True)
    
    def perform_create(self, serializer):
        """Create event with current user as organizer."""
        # FIX: Check if user is authenticated
        if not self.request.user.is_authenticated:
            # Use return, not raise!
            return
        # Save with authenticated user
        serializer.save(organizer=self.request.user)


class EventDetailView(generics.RetrieveAPIView):
    """Retrieve event details."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


class EventUpdateView(generics.UpdateAPIView):
    """Update an event (organizer only)."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOrganizerOrReadOnly]


class EventDeleteView(generics.DestroyAPIView):
    """Delete an event (organizer only)."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOrganizerOrReadOnly]


class RSVPCreateView(generics.CreateAPIView):
    """Create an RSVP for an event."""
    serializer_class = RSVPSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, event_id):
        """Create RSVP for event."""
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if RSVP.objects.filter(event=event, user=request.user).exists():
            return Response(
                {'error': 'You have already RSVP\'d to this event.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request, 'event': event}
        )
        serializer.is_valid(raise_exception=True)
        rsvp = serializer.save()
        rsvp.user = request.user
        rsvp.event = event
        rsvp.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RSVPUpdateView(generics.UpdateAPIView):
    """Update RSVP status."""
    serializer_class = RSVPSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']
    
    def patch(self, request, event_id, user_id):
        """Update RSVP status."""
        if request.user.id != user_id:
            return Response(
                {'error': 'You can only update your own RSVP.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            rsvp = RSVP.objects.get(event_id=event_id, user_id=user_id)
        except RSVP.DoesNotExist:
            return Response(
                {'error': 'RSVP not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
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
        """Create review for event - requires authentication."""
        if not request.user or not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required to create reviews'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if Review.objects.filter(event=event, user=request.user).exists():
            return Response(
                {'error': 'You have already reviewed this event.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request, 'event': event}
        )
        serializer.is_valid(raise_exception=True)
        review = serializer.save()
        review.user = request.user
        review.event = event
        review.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
