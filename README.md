# Django Blog Platform with Comments, Search, Notifications, and REST API

Welcome to the **Django Blog Platform**. This project is built using Django and Django REST Framework (DRF) to manage blog posts, comments, notifications (buzz), search functionality, and REST APIs with JWT-based authentication. The platform is designed with a focus on clarity, modularity, and best practices.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [License](#license)

## Features
- **Blog Management**: Users can create, update, and delete blog posts.
- **Comment System**: Users can comment on posts, reply to comments, update and delete their comments.
- **Notifications (Buzz)**: Users receive notifications when other users interact with their posts.
- **Dynamic Search**: Users can search for blog posts dynamically as they type.
- **Password Reset**: Users can reset their password through email.
- **JWT Authentication**: Secured endpoints using JSON Web Tokens (JWT).
- **Permissions**: Custom permissions ensure users can only edit/delete their own posts and comments.
- **Responsive**: Designed to work well across various devices.
- **Pagination**: Blog posts and comments are paginated for performance and usability.

## Tech Stack
- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT via `djangorestframework-simplejwt`
- **Front-End**: Basic templates with minimal HTML, CSS (TailwindCSS), and JavaScript for dynamic interactions
- **Testing**: Django’s test framework and REST API testing

## Project Structure

```plaintext
├── blog/
│   ├── blogs/               # Blog app: handles blog posts
│   ├── comments/            # Comments app: handles post comments
│   ├── core/                # Core app: common utilities and base templates
│   ├── search/              # Search app: dynamic search for blog posts
│   ├── buzz/                # Buzz app: notification system for user interactions
│   ├── api/                 # API app: REST API implementation
│   ├── users/               # User management and authentication
│   ├── templates/           # Centralized templates for all apps
│   └── static/              # Static files (CSS, JS, etc.)

```

## Installation
### Prerequisites

- Python 3.x
- PostgreSQL
- Git

### Steps

- **Clone the Repository**:

```bash
git clone https://github.com/hmursaleen/nest.git
cd blog
```

- **Create and activate a virtual environment**:

```bash

python3 -m venv environemt_name
source environemt_name/bin/activate  # On Windows: environemt_name\Scripts\activate
```

- **Install the dependencies**:

```bash

pip install -r requirements.txt
```

- **Set up the database**:

- Install PostgreSQL and create a new database.
- Update the DATABASES setting in settings.py with your database credentials.


- **Apply migrations**:

```bash

python manage.py migrate
```

- **Create a superuser**:

```bash
python manage.py createsuperuser
```

- **Run the development server**:

```bash
python manage.py runserver
```

- **Environment Variables**

Make sure to create a .env file in the project root with the following variables:

```plaintext

SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

## Usage
```plaintext
- Access the Admin Panel:

URL: /admin/
Log in with your superuser credentials to manage content.
```

## API Endpoints:
```plaintext
You can access the API endpoints for posts, comments, etc., under /api/.
User Authentication:

Register, login, and retrieve JWT tokens using the /api/auth/ endpoint.
```

## Testing

- Run the following command to execute the test suite:

```bash
python manage.py test
```

**The tests include**:

- Unit tests for views, models, and forms
- API tests for CRUD operations (Blog posts, Comments)
- JWT Authentication and permission tests


## API Documentation

- The API is built using Django REST Framework, and all the endpoints are well-documented. To explore the API, visit the following:

**/api/docs/**

**Available Endpoints**:
- Blog Posts: /api/blogs/posts
- Comments: /api/comments/comments
- JWT Auth: /api/auth/


## Deployment

- To deploy the project, follow these general steps:

- Set up a production database (e.g., PostgreSQL on the cloud).

- Configure environment variables for production (e.g., turn off DEBUG).

- Set up a WSGI server (e.g., Gunicorn) and a reverse proxy server (e.g., Nginx).

- Collect static files:

```bash
python manage.py collectstatic
```

**Deploy to a cloud platform like Heroku, AWS, or DigitalOcean.**