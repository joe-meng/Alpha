# -- coding: utf-8 --
import logging
import os
import sys

import django


def init_project():
    root_path = os.path.abspath(__file__ if '__file__' in locals() else os.path.curdir)
    while os.path.basename(root_path).lower() != 'alpha':
        root_path = os.path.dirname(root_path)

    root_path = os.path.join(root_path, 'src')
    sys.path.append(os.path.join(root_path, 'api'))
    sys.path.append(root_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alpha.settings.prod")
    django.setup()

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] %(name)s:%(lineno)d %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info((' Init Django with profile: %s ' %
                  os.environ.get('DJANGO_SETTINGS_MODULE')).center(80, '-'))

init_project()