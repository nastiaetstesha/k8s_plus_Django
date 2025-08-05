"""
WSGI config for Django webapp.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys
import traceback

with open("/tmp/wsgi_log.txt", "w") as f:
    try:
        f.write("PYTHONPATH: {}\n".format(os.environ.get("PYTHONPATH")))
        f.write("sys.path:\n" + "\n".join(sys.path) + "\n")
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
    except Exception:
        f.write("ERROR:\n")
        f.write(traceback.format_exc())

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')

application = get_wsgi_application()
