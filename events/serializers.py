from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(source='organizer.username', read_only=True)
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'organizer_name', 
                  'location', 'start_time', 'end_time', 'created_at']
        read_only_fields = ['organizer_name', 'created_at']
