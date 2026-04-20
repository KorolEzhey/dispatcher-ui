import os
import sys

path = '/home/YOUR_USERNAME/dispatcher-ui/admin_site'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'admin_site.settings'
os.environ['DEBUG'] = '0'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
