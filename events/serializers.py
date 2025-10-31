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
        try:
            return obj.rsvps.count()
        except:
            return 0
    
    def get_average_rating(self, obj):
        """Get average rating for event."""
        try:
            reviews = obj.reviews.all()
            if not reviews.exists():
                return None
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        except:
            return None


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
