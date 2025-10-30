from urllib import response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from .models import Event
from .serializers import EventSerializer
from .permissions import IsOrganizerOrReadOnly
from .models import Event, RSVP
from .serializers import EventSerializer, RSVPSerializer
from rest_framework.response import Response

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.filter(is_public=True)
    serializer_class = EventSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]

class EventUpdateView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOrganizerOrReadOnly]

class EventDeleteView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOrganizerOrReadOnly]

class RSVPCreateView(generics.CreateAPIView):
    serializer_class = RSVPSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response({'error': 'Event not found.'}, status=404)
        
        # Check if RSVP already exists
        if RSVP.objects.filter(event=event, user=request.user).exists():
            return Response({'error': 'You have already RSVP\'d to this event.'}, status=400)
        
        serializer = self.get_serializer(data=request.data, context={'request': request, 'event': event})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=201)
