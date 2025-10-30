from rest_framework import serializers
from .models import Event
from .models import Event, RSVP

class EventSerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(source='organizer.username', read_only=True)
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'organizer', 'organizer_name',
                  'location', 'start_time', 'end_time', 'is_public', 'created_at']
        read_only_fields = ['organizer', 'created_at']
    
    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError({
                'end_time': 'End time must be after start time.'
            })
        return data
    
    def create(self, validated_data):
        validated_data['organizer'] = self.context['request'].user
        return super().create(validated_data)

class RSVPSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = RSVP
        fields = ['id', 'event', 'user_name', 'status', 'created_at']
        read_only_fields = ['user_name', 'created_at']