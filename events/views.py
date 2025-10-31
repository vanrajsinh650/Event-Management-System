from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

from .models import Event, RSVP, Review
from .serializers import EventSerializer, RSVPSerializer, ReviewSerializer
from .permissions import IsOrganizerOrReadOnly


class EventListCreateView(generics.ListCreateAPIView):
    """List all public events or create a new event."""
    queryset = Event.objects.filter(is_public=True)
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['location', 'is_public']
    search_fields = ['title', 'description', 'organizer__username']
    ordering_fields = ['start_time', 'created_at']
    ordering = ['-start_time']
    
    def perform_create(self, serializer):
        """Create event with authenticated user as organizer."""
        serializer.save(organizer=self.request.user)


class EventDetailView(generics.RetrieveAPIView):
    """Retrieve event details."""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


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
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if RSVP.objects.filter(event=event, user=request.user).exists():
            return Response({'error': 'Already RSVP\'d'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, event=event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RSVPUpdateView(generics.UpdateAPIView):
    """Update RSVP status."""
    serializer_class = RSVPSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']
    
    def patch(self, request, event_id, user_id):
        if request.user.id != user_id:
            return Response({'error': 'Cannot update others RSVP'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            rsvp = RSVP.objects.get(event_id=event_id, user_id=user_id)
        except RSVP.DoesNotExist:
            return Response({'error': 'RSVP not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(rsvp, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ReviewListCreateView(generics.ListCreateAPIView):
    """List/Create reviews for an event."""
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        return Review.objects.filter(event_id=event_id)
    
    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if Review.objects.filter(event=event, user=request.user).exists():
            return Response({'error': 'Already reviewed'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, event=event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
