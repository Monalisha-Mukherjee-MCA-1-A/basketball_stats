"""
ASGI config for basketball_stats project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'basketball_stats.settings')

application = get_asgi_application()
