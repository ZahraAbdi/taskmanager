# Task Management System

A Django REST Framework API for managing projects, tasks, and team collaboration with JWT authentication.

## Tech Stack

- Django REST Framework
- PostgreSQL database
- JWT authentication (djangorestframework-simplejwt)
- Docker & Docker Compose

## Features

### User Management
- User registration and authentication
- JWT-based secure login with access and refresh tokens
- Password management (change, forgot, reset via email)
- User profile management
- Role-based access control (Admin, Manager, Developer)

### Project Management
- Create, view, update, and delete projects
- Add and remove team members
- View projects by user
- Admin-controlled project creation

### Task Management
- Create and assign tasks to users
- Assign tasks to projects
- Track task status (To Do, In Progress, Done)
- Set task priorities (Low, Medium, High)
- Set due dates and track overdue tasks
- View tasks by user or project
- Filter tasks by status, priority, and project


## Installation

### Prerequisites
- Docker and Docker Compose
- Git

### Setup

1. Clone the repository
```bash
git clone https://github.com/ZahraAbdi/taskmanager
cd backend
```

2. Configure environment variables

Create a `.env` file in the project root:
```env
# Database
POSTGRES_DB=taskmanagement
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432

# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email (for password reset)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Frontend
FRONTEND_URL=http://localhost:3000
```

3. Build and run with Docker
```bash
docker-compose up --build
```

4. Run database migrations
```bash
docker-compose exec web python manage.py migrate
```

5. Create a superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

6. Access the application
- API: http://localhost:8000/api/
- Admin Panel: http://localhost:8000/admin/

## API Endpoints

### Authentication
`/api/accounts/`

- `POST /register/` - Register a new user
- `POST /login/` - Login and receive JWT tokens
- `POST /logout/` - Logout and blacklist refresh token
- `POST /forgot-password/` - Request password reset email
- `POST /reset-password/` - Reset password with token
- `POST /token/refresh/` - Refresh access token
- `GET /profile/` - Get user profile
- `PUT /profile/` - Update user profile
- `POST /change-password/` - Change password
- `GET /` - List all users (Admin only)
- `GET /users/<user_id>/tasks/` - Get tasks for specific user

### Projects
`/api/projects/`

- `GET /` - List all projects
- `POST /` - Create new project (Admin only)
- `GET /my/` - Get current user's projects
- `GET /user/<user_id>/` - Get specific user's projects
- `GET /<project_id>/` - Get project details
- `PUT /<project_id>/` - Update project (Admin only)
- `DELETE /<project_id>/` - Delete project (Admin only)
- `GET /<project_id>/members/` - Get project members
- `POST /<project_id>/members/` - Add member to project (Admin only)
- `DELETE /<project_id>/members/` - Remove member from project (Admin only)
- `POST /<project_id>/tasks/add/` - Assign task to project

### Tasks
`/api/tasks/`

- `GET /` - List all tasks
- `POST /` - Create new task
- `GET /my/` - Get current user's tasks
- `GET /user/<user_id>/` - Get specific user's tasks
- `GET /<task_id>/` - Get task details
- `PUT /<task_id>/` - Update task
- `DELETE /<task_id>/` - Delete task
- `GET /<task_id>/comments/` - Get task comments
- `POST /<task_id>/comments/` - Add comment to task
- `GET /comments/<comment_id>/` - Get comment details
- `PUT /comments/<comment_id>/` - Update comment
- `DELETE /comments/<comment_id>/` - Delete comment

## Authentication Flow

Login to get your tokens:
```bash
POST /api/accounts/login/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "role": "developer"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

Use the access token in your requests:
```
Authorization: Bearer <access_token>
```

Refresh your token when it expires:
```bash
POST /api/accounts/token/refresh/
Content-Type: application/json

{
  "refresh": "your_refresh_token"
}
```

## Usage Examples

Create a project:
```bash
POST /api/projects/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Website Redesign",
  "description": "Redesign company website",
  "member_ids": ["user-uuid-1", "user-uuid-2"]
}
```

Create a task:
```bash
POST /api/tasks/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "title": "Design homepage",
  "description": "Create homepage mockup",
  "assigned_to": "user-uuid",
  "due_date": "2026-03-15T12:00:00Z",
  "status": "todo",
  "priority": "high"
}
```

Filter your tasks:
```bash
GET /api/tasks/my/?status=in_progress&priority=high
Authorization: Bearer <access_token>
```

Add a member to a project:
```bash
POST /api/projects/<project_id>/members/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "user_id": "user-uuid"
}
```

## User Roles

- Admin: Full access to all features, can create/edit/delete projects and manage users
- Manager: Can view all projects and tasks, manage team members
- Developer: Can view assigned tasks and projects
