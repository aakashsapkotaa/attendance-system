# Attendance Management System

A comprehensive attendance management system built with Django, featuring face recognition for automated attendance tracking.

## Features

- Face Recognition based attendance
- User Authentication and Authorization
- Real-time attendance tracking
- Excel report generation
- Admin dashboard
- Student/Employee management
- Course/Department management

## Tech Stack

- Python 3.8+
- Django 5.0.2
- MySQL
- OpenCV
- dlib
- face_recognition
- Bootstrap
- jQuery

## Prerequisites

- Python 3.8 or higher
- MySQL Server
- WAMP Server (for Windows)
- Git

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/attendance-system.git
cd attendance-system
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure MySQL:
- Open MySQL command line or phpMyAdmin
- Create database:
```sql
CREATE DATABASE attendance_system;
```

5. Update database settings in `attendance_system/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'attendance_system',
        'USER': 'root',
        'PASSWORD': '',  # Your MySQL password
        'HOST': 'localhost',
        'PORT': '3308',  # Your MySQL port
    }
}
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Create superuser:
```bash
python manage.py createsuperuser
```

8. Run the development server:
```bash
python manage.py runserver
```

## Free Hosting Options

### 1. PythonAnywhere (Recommended for Django)
1. Sign up at [PythonAnywhere](https://www.pythonanywhere.com/)
2. Upload your code or clone from GitHub
3. Set up virtual environment and install dependencies
4. Configure MySQL database
5. Set up your web app in the Web tab
6. Your site will be available at `yourusername.pythonanywhere.com`

### 2. Render
1. Sign up at [Render](https://render.com/)
2. Connect your GitHub repository
3. Create a new Web Service
4. Configure build and start commands
5. Add environment variables
6. Deploy

### 3. Railway
1. Sign up at [Railway](https://railway.app/)
2. Connect your GitHub repository
3. Add MySQL service
4. Configure environment variables
5. Deploy

## Deployment Steps

1. Update settings.py for production:
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# Add security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

2. Collect static files:
```bash
python manage.py collectstatic
```

3. Set up environment variables:
```bash
export DJANGO_SECRET_KEY='your-secret-key'
export DATABASE_URL='your-database-url'
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, email your-email@example.com or open an issue in the GitHub repository. 