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

class RSVPUpdateView(generics.UpdateAPIView):
    serializer_class = RSVPSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']
    
    def patch(self, request, event_id, user_id):
        if request.user.id != user_id:
            return Response({'error': 'You can only update your own RSVP.'}, status=403)
        
        try:
            rsvp = RSVP.objects.get(event_id=event_id, user_id=user_id)
        except RSVP.DoesNotExist:
            return Response({'error': 'RSVP not found.'}, status=404)
        
        serializer = self.get_serializer(rsvp, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
