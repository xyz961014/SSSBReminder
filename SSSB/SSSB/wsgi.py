"""
WSGI config for THUfootball project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import sys
from os.path import join,dirname,abspath
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SSSB.settings')

 
PROJECT_DIR = dirname(dirname(abspath(__file__)))#3
sys.path.insert(0, PROJECT_DIR) # 5
 
os.environ["DJANGO_SETTINGS_MODULE"] = "SSSB.settings" # 7
 
application = get_wsgi_application()
