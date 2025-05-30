import os
import sys
import subprocess
import platform

def print_colored(text, color):
    """Print colored text for windows cmd."""
    colors = {
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'reset': '\033[0m'
    }
    print(f"{colors.get(color, '')}{text}{colors['reset']}")

def run_command(command):
    """Run a command and return its output."""
    try:
        result = subprocess.run(command, shell=True, check=True, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                               text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_module(module_name):
    """Check if a Python module is installed."""
    try:
        __import__(module_name)
        print_colored(f"{module_name}: Installed", "green")
        return True
    except ImportError:
        print_colored(f"{module_name}: Not installed", "red")
        return False

def setup_virtual_env():
    """Set up and activate the virtual environment."""
    if not os.path.exists("venv"):
        print_colored("Creating virtual environment...", "yellow")
        success, output = run_command("python -m venv venv")
        if not success:
            print_colored("Failed to create virtual environment!", "red")
            print(output)
            return False
    
    # Set environment variables
    os.environ["VIRTUAL_ENV"] = os.path.abspath("venv")
    return True

def install_dependencies():
    """Install required dependencies."""
    print_colored("Installing dependencies...", "yellow")
    
    # Core dependencies with specific versions for stability
    packages = [
        "Django==5.0.2",
        "mysqlclient==2.2.0",
        "Pillow==10.0.1",
        "numpy==1.24.3",
        "XlsxWriter==3.1.0",
        "python-dateutil==2.8.2",
        "opencv-python==4.8.0.76",
        "dlib==19.24.2",
        "face-recognition==1.3.0"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        success, output = run_command(f"pip install {package}")
        if not success:
            print_colored(f"Failed to install {package}!", "red")
            print(output)

def check_mysql_connection():
    """Check MySQL connection using Django."""
    print_colored("Checking MySQL connection...", "yellow")
    
    try:
        import django
        from django.conf import settings
        
        # Set up Django environment
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')
        django.setup()
        
        # Check database connection
        from django.db import connections
        from django.db.utils import OperationalError
        
        try:
            conn = connections['default']
            conn.cursor()
            print_colored("MySQL connection successful!", "green")
            return True
        except OperationalError as e:
            print_colored(f"Error connecting to MySQL: {e}", "red")
            print("Please check if:")
            print("1. Your MySQL server is running")
            print("2. The database 'attendance_system' exists")
            print("3. The username and password in settings.py are correct")
            return False
            
    except ImportError:
        print_colored("Django not installed correctly. Please run setup first.", "red")
        return False

def run_migrations():
    """Run Django migrations."""
    print_colored("Running migrations...", "yellow")
    
    commands = [
        "python manage.py makemigrations",
        "python manage.py migrate"
    ]
    
    for command in commands:
        print(f"Running: {command}")
        success, output = run_command(command)
        if not success:
            print_colored(f"Failed to run {command}!", "red")
            print(output)
            return False
    
    print_colored("Migrations completed successfully!", "green")
    return True

def start_server():
    """Start the Django development server."""
    print_colored("Starting development server...", "green")
    print("Access the application at http://127.0.0.1:8000/")
    print("Press Ctrl+C to stop the server")
    
    success, output = run_command("python manage.py runserver")
    if not success:
        print_colored("Failed to start server!", "red")
        print(output)

def main():
    print_colored("Attendance Management System Setup", "green")
    print("=" * 40)
    
    # Setup virtual environment
    if not setup_virtual_env():
        return
    
    # Check dependencies
    print_colored("\nChecking required modules:", "yellow")
    modules = ["django", "MySQLdb", "PIL", "numpy", "xlsxwriter", "cv2", "face_recognition", "dlib"]
    missing_modules = []
    
    for module in modules:
        if not check_module(module):
            missing_modules.append(module)
    
    # Install missing dependencies
    if missing_modules:
        print_colored("\nInstalling missing dependencies...", "yellow")
        install_dependencies()
    
    # Check MySQL connection
    if not check_mysql_connection():
        return
    
    # Run migrations
    if not run_migrations():
        return
    
    # Ask to start server
    print("\nSetup completed successfully!")
    start_choice = input("Do you want to start the server now? (y/n): ").lower()
    
    if start_choice == 'y':
        start_server()
    else:
        print("\nYou can start the server later with:")
        print("python manage.py runserver")

if __name__ == "__main__":
    main() 