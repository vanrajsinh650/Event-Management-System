# Event Management System API

A comprehensive, production-ready Event Management System API built with Django REST Framework, featuring JWT authentication, event CRUD operations, RSVP management, reviews, and asynchronous email notifications.

## 🚀 Features

- **User Management**
  - User registration and authentication
  - JWT token-based authentication
  - User profiles with profile pictures
  
- **Event Management**
  - Create, read, update, and delete events
  - Public and private events with access control
  - Event filtering by location, organizer, and visibility
  - Search events by title and description
  - Pagination support

- **RSVP System**
  - RSVP to events with status (Going, Maybe, Not Going)
  - Update RSVP status
  - Unique RSVP per user per event
  - Organizers cannot RSVP to their own events

- **Review System**
  - Rate and review events (1-5 stars)
  - View all reviews for an event
  - One review per user per event

- **Async Notifications**
  - Celery-based email notifications
  - Notify organizers of new RSVPs
  - Notify organizers of new reviews

- **API Documentation**
  - Auto-generated Swagger/OpenAPI documentation
  - Interactive API explorer
  - ReDoc documentation

## 🛠 Technology Stack

- **Backend**: Django 4.2, Django REST Framework 3.14
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite (easily configurable to PostgreSQL/MySQL)
- **Task Queue**: Celery 5.4 with Redis broker
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **Testing**: pytest, pytest-django
- **Image Processing**: Pillow
- **Environment Management**: python-decouple

## 📋 Prerequisites

- Python 3.8 or higher
- Redis server (for Celery)
- pip and virtualenv

## 🔧 Installation

### 1. Clone the repository

\`\`\`bash
git clone <repository-url>
cd event_management
\`\`\`

### 2. Create and activate virtual environment

\`\`\`bash
python3 -m venv .venv
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate  # On Windows
\`\`\`

### 3. Install dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Create .env file

\`\`\`bash
cp .env.example .env
\`\`\`

Edit \`.env\` and configure your settings:

\`\`\`env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration (for notifications)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
\`\`\`

### 5. Run migrations

\`\`\`bash
python manage.py makemigrations user
python manage.py makemigrations events
python manage.py migrate
\`\`\`

### 6. Create superuser (optional)

\`\`\`bash
python manage.py createsuperuser
\`\`\`

### 7. Run the development server

\`\`\`bash
python manage.py runserver
\`\`\`

The API will be available at \`http://localhost:8000/\`

### 8. Start Redis (in a new terminal)

\`\`\`bash
redis-server
\`\`\`

### 9. Start Celery worker (in a new terminal)

\`\`\`bash
# Activate virtual environment first
source .venv/bin/activate

# Start Celery worker
celery -A event_management worker --loglevel=info
\`\`\`

## 📚 API Documentation

Once the server is running, access the API documentation:

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **JSON Schema**: http://localhost:8000/swagger.json

## 🔑 Authentication

### 1. Register a new user

\`\`\`bash
curl -X POST http://localhost:8000/api/register/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe"
  }'
\`\`\`

### 2. Obtain JWT tokens

\`\`\`bash
curl -X POST http://localhost:8000/api/token/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "username": "johndoe",
    "password": "SecurePass123!"
  }'
\`\`\`

Response:
\`\`\`json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
\`\`\`

### 3. Use the access token in requests

\`\`\`bash
curl -X GET http://localhost:8000/api/events/ \\
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
\`\`\`

### 4. Refresh access token

\`\`\`bash
curl -X POST http://localhost:8000/api/token/refresh/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "refresh": "YOUR_REFRESH_TOKEN"
  }'
\`\`\`

## 📖 API Endpoints

### Authentication
- \`POST /api/register/\` - Register new user
- \`POST /api/token/\` - Obtain JWT tokens
- \`POST /api/token/refresh/\` - Refresh access token
- \`GET /api/profile/\` - Get current user profile
- \`PUT /api/profile/\` - Update current user profile

### Events
- \`GET /api/events/\` - List all public events (with pagination, filtering, search)
- \`POST /api/events/\` - Create new event (authenticated)
- \`GET /api/events/{id}/\` - Get event details
- \`PUT /api/events/{id}/\` - Update event (organizer only)
- \`PATCH /api/events/{id}/\` - Partial update event (organizer only)
- \`DELETE /api/events/{id}/\` - Delete event (organizer only)

### RSVPs
- \`POST /api/events/{event_id}/rsvp/\` - Create RSVP
- \`PATCH /api/events/{event_id}/rsvp/{user_id}/\` - Update RSVP status

### Reviews
- \`GET /api/events/{event_id}/reviews/\` - List all reviews for event
- \`POST /api/events/{event_id}/reviews/\` - Create review for event

## 🔍 Query Parameters

### Event Filtering
- \`?location=Mumbai\` - Filter by location
- \`?organizer=1\` - Filter by organizer ID
- \`?is_public=true\` - Filter by visibility
- \`?search=conference\` - Search in title and description
- \`?ordering=-start_time\` - Order by start time (descending)
- \`?page=2\` - Pagination (10 items per page)

## 🧪 Running Tests

\`\`\`bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest events/tests.py

# Run with coverage report
pytest --cov=.

# Generate HTML coverage report
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser
\`\`\`

## 📁 Project Structure

\`\`\`
event_management/
├── event_management/
│   ├── __init__.py          # Celery app initialization
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── celery.py            # Celery configuration
│   ├── asgi.py
│   └── wsgi.py
├── events/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py             # Admin configuration
│   ├── apps.py
│   ├── models.py            # Event, RSVP, Review models
│   ├── permissions.py       # Custom permissions
│   ├── serializers.py       # DRF serializers
│   ├── tasks.py             # Celery tasks
│   ├── tests.py             # All tests
│   ├── urls.py              # Event URL patterns
│   └── views.py             # API views
├── user/                    # Note: singular 'user'
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py             # Admin configuration
│   ├── apps.py
│   ├── models.py            # UserProfile model
│   ├── serializers.py       # User serializers
│   ├── views.py             # User views
│   └── urls.py              # User URL patterns
├── .venv/                   # Virtual environment
├── media/                   # User-uploaded files
├── staticfiles/             # Static files
├── .env                     # Environment variables
├── .gitignore
├── db.sqlite3               # SQLite database
├── manage.py                # Django management script
├── pytest.ini               # Pytest configuration
├── README.md                # This file
└── requirements.txt         # Python dependencies
\`\`\`

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| \`SECRET_KEY\` | Django secret key | Required |
| \`DEBUG\` | Debug mode | \`True\` |
| \`ALLOWED_HOSTS\` | Allowed hosts | \`localhost,127.0.0.1\` |
| \`EMAIL_BACKEND\` | Email backend | \`console.EmailBackend\` |
| \`EMAIL_HOST\` | SMTP host | \`smtp.gmail.com\` |
| \`EMAIL_PORT\` | SMTP port | \`587\` |
| \`EMAIL_USE_TLS\` | Use TLS | \`True\` |
| \`EMAIL_HOST_USER\` | Email username | Empty |
| \`EMAIL_HOST_PASSWORD\` | Email password | Empty |
| \`CELERY_BROKER_URL\` | Celery broker URL | \`redis://localhost:6379/0\` |
| \`CELERY_RESULT_BACKEND\` | Celery result backend | \`redis://localhost:6379/0\` |

## 🛡 Security Features

- JWT-based authentication with token refresh
- Password validation and hashing
- Permission-based access control
- CSRF protection
- SQL injection protection (Django ORM)
- XSS protection
- Private event access control

## 📝 Example Usage

### Create an Event

\`\`\`python
import requests

headers = {
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
    'Content-Type': 'application/json'
}

data = {
    "title": "Django Conference 2025",
    "description": "Annual Django developers conference",
    "location": "Mumbai, India",
    "start_time": "2025-11-15T09:00:00Z",
    "end_time": "2025-11-15T17:00:00Z",
    "is_public": True
}

response = requests.post(
    'http://localhost:8000/api/events/',
    json=data,
    headers=headers
)

print(response.json())
\`\`\`

### RSVP to an Event

\`\`\`python
headers = {
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
    'Content-Type': 'application/json'
}

data = {
    "status": "Going"
}

response = requests.post(
    'http://localhost:8000/api/events/1/rsvp/',
    json=data,
    headers=headers
)

print(response.json())
\`\`\`

### Add a Review

\`\`\`python
headers = {
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
    'Content-Type': 'application/json'
}

data = {
    "rating": 5,
    "comment": "Excellent event! Very well organized."
}

response = requests.post(
    'http://localhost:8000/api/events/1/reviews/',
    json=data,
    headers=headers
)

print(response.json())
\`\`\`

## 🐛 Troubleshooting

### Redis Connection Error
If Celery can't connect to Redis:
\`\`\`bash
# Check if Redis is running
redis-cli ping
# Should return: PONG

# Start Redis if not running
redis-server
\`\`\`

### Database Errors
\`\`\`bash
# Reset database
rm db.sqlite3
python manage.py migrate
\`\`\`

### Import Errors
\`\`\`bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
\`\`\`

## 📦 .gitignore

\`\`\`gitignore
# Python
*.py[cod]
*$py.class
*.so
.Python
__pycache__/
*.egg-info/
.venv/
venv/

# Django
*.log
db.sqlite3
media/
staticfiles/

# Environment
.env

# IDE
.vscode/
.idea/

# Testing
.pytest_cache/
htmlcov/
.coverage

# Celery
celerybeat-schedule
\`\`\`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (\`git checkout -b feature/AmazingFeature\`)
3. Commit your changes (\`git commit -m 'Add some AmazingFeature'\`)
4. Push to the branch (\`git push origin feature/AmazingFeature\`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

Your Name - vanrajsolanki2875@gmail.com

## 🙏 Acknowledgments

- Django REST Framework documentation
- djangorestframework-simplejwt
- Celery documentation
- drf-yasg for API documentation

---
