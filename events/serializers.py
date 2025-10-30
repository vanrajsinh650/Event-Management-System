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
        read_only_fields = ['id', 'organizer', 'created_at', 'updated_at', 'rsvp_count', 'average_rating']
    
    def get_rsvp_count(self, obj):
        """Get total RSVPs for event."""
        # Updated to handle both model instances and dicts (OrderedDict) returned during serialization of validated_data.
        # Safely computes length using .get('rsvps') when obj has no attribute.
        if isinstance(obj, dict):
            return len(obj.get('rsvps', []))
        return obj.rsvps.count() if hasattr(obj, 'rsvps') else 0
    
    def get_average_rating(self, obj):
        """Get average rating for event."""
        reviews = obj.reviews.all()
        if not reviews:
            return None
        return round(sum(r.rating for r in reviews) / len(reviews), 1)
    
    def validate(self, data):
        """Validate event times."""
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        
        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError({
                'end_time': 'End time must be after start time.'
            })
        return data


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
