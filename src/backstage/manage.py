#!/usr/bin/env python
import os
import sys

root_path = os.path.abspath(__file__)
while os.path.basename(root_path) != 'src':
    root_path = os.path.dirname(root_path)
if root_path not in sys.path:
    sys.path.append(root_path)
api_path = os.path.join(root_path, 'api')
if api_path not in sys.path:
    sys.path.append(api_path)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backstage.settings.defaults")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
