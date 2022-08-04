#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acuest.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    arguments = []

    if sys.argv:
        for arg in sys.argv:
            if arg == 'prod':
                os.environ.setdefault('env', '.prod.env')
            else:
                arguments.append(arg) 
    execute_from_command_line(arguments)


if __name__ == '__main__':
    main()
