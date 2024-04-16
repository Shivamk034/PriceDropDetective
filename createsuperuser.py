import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PriceDropDetective.settings")
django.setup()

import os
from django.contrib.auth.models import User

try:
    User.objects.get(username=os.environ["ADMIN_USERNAME"])

except:
    user = User(username=os.environ["ADMIN_USERNAME"],
            email=os.environ["ADMIN_EMAIL"],
            is_staff=True,
            is_superuser=True,
            is_active=True,
            )


    user.set_password(os.environ["ADMIN_PASSWORD"])
    user.save()
