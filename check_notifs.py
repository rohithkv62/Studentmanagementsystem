import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smsproj.settings')
django.setup()

from smsapp.models import Notification

count = Notification.objects.count()
print(f"Total notifications: {count}")
