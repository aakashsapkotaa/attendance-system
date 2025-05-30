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

def check_python_version():
    """Check if Python version is compatible."""
    required_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        print_colored(f"Python {required_version[0]}.{required_version[1]} or higher is required", "red")
        return False
    return True

def setup_virtual_env():
    """Create and activate virtual environment."""
    if not os.path.exists("venv"):
        print_colored("Creating virtual environment...", "yellow")
        success, output = run_command("python -m venv venv")
        if not success:
            print_colored("Failed to create virtual environment!", "red")
            print(output)
            return False
    return True

def install_dependencies():
    """Install all required dependencies."""
    print_colored("Installing dependencies...", "yellow")
    
    # Upgrade pip first
    run_command("python -m pip install --upgrade pip")
    
    # Install requirements
    success, output = run_command("pip install -r requirements.txt")
    if not success:
        print_colored("Failed to install dependencies!", "red")
        print(output)
        return False
    
    print_colored("All dependencies installed successfully!", "green")
    return True

def check_mysql():
    """Check if MySQL is installed and running."""
    print_colored("Checking MySQL installation...", "yellow")
    
    try:
        import MySQLdb
        print_colored("MySQL client is installed", "green")
    except ImportError:
        print_colored("MySQL client is not installed!", "red")
        print("Please install MySQL server and client first.")
        return False
    
    return True

def main():
    print_colored("Attendance System Installation", "green")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Setup virtual environment
    if not setup_virtual_env():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Check MySQL
    if not check_mysql():
        return
    
    print_colored("\nInstallation completed successfully!", "green")
    print("\nNext steps:")
    print("1. Make sure MySQL server is running")
    print("2. Create database 'attendance_system'")
    print("3. Update database settings in attendance_system/settings.py")
    print("4. Run migrations: python manage.py migrate")
    print("5. Start server: python manage.py runserver")

if __name__ == "__main__":
    main() 