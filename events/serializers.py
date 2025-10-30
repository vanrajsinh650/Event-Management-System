from rest_framework import serializers
from .models import Event
from .models import Event, RSVP
from .models import Event, RSVP, Review

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
    event_title = serializers.CharField(source='event.title', read_only=True)
    
    class Meta:
        model = RSVP
        fields = ['id', 'event', 'user', 'user_name', 'event_title', 'status', 'created_at']
        read_only_fields = ['user', 'event', 'created_at']
    
    def validate(self, attrs):
        request = self.context.get('request')
        event = self.context.get('event')
        
        if event and request and event.organizer == request.user:
            raise serializers.ValidationError({
                'error': 'Event organizer cannot RSVP to their own event.'
            })
        return attrs
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['event'] = self.context['event']
        return super().create(validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'event', 'user', 'user_name', 'event_title', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'event', 'created_at']
    
    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['event'] = self.context['event']
        return super().create(validated_data)
