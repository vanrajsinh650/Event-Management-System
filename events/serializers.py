"""
Serializers for event-related models.
"""
from rest_framework import serializers
from .models import Event, RSVP, Review


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model."""
    organizer_name = serializers.CharField(source='organizer.username', read_only=True)
    rsvp_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'organizer', 'organizer_name',
            'location', 'start_time', 'end_time', 'is_public', 'created_at',
            'updated_at', 'rsvp_count', 'average_rating'
        ]
        read_only_fields = ['id', 'organizer', 'created_at', 'updated_at']
    
    def get_rsvp_count(self, obj):
        """Get total RSVPs for event."""
        return obj.rsvps.count()
    
    def get_average_rating(self, obj):
        """Get average rating for event."""
        reviews = obj.reviews.all()
        if not reviews:
            return None
        return sum(r.rating for r in reviews) / len(reviews)
    
    def validate(self, data):
        """Validate event times."""
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError({
                'end_time': 'End time must be after start time.'
            })
        return data
    
    def create(self, validated_data):
        """Create event with current user as organizer."""
        validated_data['organizer'] = self.context['request'].user
        return super().create(validated_data)


class RSVPSerializer(serializers.ModelSerializer):
    """Serializer for RSVP model."""
    user_name = serializers.CharField(source='user.username', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    
    class Meta:
        model = RSVP
        fields = [
            'id', 'event', 'user', 'user_name', 'event_title', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'event', 'created_at']
    
    def validate(self, attrs):
        """Validate RSVP constraints."""
        request = self.context.get('request')
        event = self.context.get('event')
        
        if event and request and event.organizer == request.user:
            raise serializers.ValidationError({
                'error': 'Event organizer cannot RSVP to their own event.'
            })
        return attrs
    
    def create(self, validated_data):
        """Create RSVP with current user."""
        validated_data['user'] = self.context['request'].user
        validated_data['event'] = self.context['event']
        return super().create(validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
    user_name = serializers.CharField(source='user.username', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'event', 'user', 'user_name', 'event_title', 'rating', 'comment', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'event', 'created_at']
    
    def validate_rating(self, value):
        """Validate rating is between 1-5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value
    
    def validate(self, attrs):
        """Validate review constraints."""
        request = self.context.get('request')
        event = self.context.get('event')
        
        if event and request and Review.objects.filter(event=event, user=request.user).exists():
            raise serializers.ValidationError({
                'error': 'You have already reviewed this event.'
            })
        return attrs
    
    def create(self, validated_data):
        """Create review with current user."""
        validated_data['user'] = self.context['request'].user
        validated_data['event'] = self.context['event']
        return super().create(validated_data)
