from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User

from .models import Event, RSVP, Review
from .serializers import EventSerializer, RSVPSerializer, ReviewSerializer


class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['location', 'is_public']
    search_fields = ['title', 'description', 'organizer__username']
    ordering_fields = ['start_time', 'created_at']
    ordering = ['-start_time']
    
    def perform_create(self, serializer):
        user = User.objects.first() or User.objects.create_user(username='admin', password='admin')
        serializer.save(organizer=user)


class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


class EventUpdateView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


class EventDeleteView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


class RSVPCreateView(generics.CreateAPIView):
    serializer_class = RSVPSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except:
            return Response({'error': 'Event not found'}, status=404)
        
        user = User.objects.first() or User.objects.create_user(username='user1', password='pass')
        
        if RSVP.objects.filter(event=event, user=user).exists():
            return Response({'error': 'Already RSVP\'d'}, status=400)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, event=event)
        return Response(serializer.data, status=201)


class RSVPUpdateView(generics.UpdateAPIView):
    serializer_class = RSVPSerializer
    permission_classes = [AllowAny]
    http_method_names = ['patch']
    
    def patch(self, request, event_id, user_id):
        try:
            rsvp = RSVP.objects.get(event_id=event_id, user_id=user_id)
        except:
            return Response({'error': 'RSVP not found'}, status=404)
        
        serializer = self.get_serializer(rsvp, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        event_id = self.kwargs.get('event_id')
        return Review.objects.filter(event_id=event_id)
    
    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except:
            return Response({'error': 'Event not found'}, status=404)
        
        user = User.objects.first() or User.objects.create_user(username='user2', password='pass')
        
        if Review.objects.filter(event=event, user=user).exists():
            return Response({'error': 'Already reviewed'}, status=400)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, event=event)
        return Response(serializer.data, status=201)
