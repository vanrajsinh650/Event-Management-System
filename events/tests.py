import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta
from events.models import Event

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def _create_user(username='testuser'):
        return User.objects.create_user(
            username=username, 
            password='testpass123',
            email=f'{username}@test.com'
        )
    return _create_user

@pytest.mark.django_db
class TestUserRegistration:
    def test_user_registration(self, api_client):
        data = {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'TestPass123!',
            'password2': 'TestPass123!'
        }
        response = api_client.post('/api/register/', data)
        assert response.status_code == 201

@pytest.mark.django_db
class TestJWTAuth:
    def test_login(self, api_client, create_user):
        user = create_user()
        response = api_client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        assert response.status_code == 200
        assert 'access' in response.data

@pytest.mark.django_db
class TestEvents:
    def test_create_event(self, api_client, create_user):
        user = create_user()
        api_client.force_authenticate(user=user)
        
        data = {
            'title': 'Test Event',
            'description': 'Test',
            'location': 'Test Location',
            'start_time': (timezone.now() + timedelta(days=1)).isoformat(),
            'end_time': (timezone.now() + timedelta(days=1, hours=2)).isoformat(),
        }
        response = api_client.post('/api/events/', data)
        assert response.status_code == 201

@pytest.mark.django_db
class TestPermissions:
    def test_organizer_can_edit(self, api_client, create_user):
        organizer = create_user(username='organizer')
        other = create_user(username='other')
        
        event = Event.objects.create(
            title='Test',
            description='Test',
            organizer=organizer,
            location='Test',
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=2)
        )
        
        api_client.force_authenticate(user=other)
        response = api_client.patch(f'/api/events/{event.id}/update/', {'title': 'Hacked'})
        assert response.status_code == 403
