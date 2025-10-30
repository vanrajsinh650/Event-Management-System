import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

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
