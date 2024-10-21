# backend/manage.py
import os
import sys

def main():
    """Run administrative tasks."""
    environment = os.getenv('DJANGO_ENV', 'local')  # 默認為本地開發環境
    if environment == 'docker':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.docker')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.local')
        
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
