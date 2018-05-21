from django.contrib.admin import AdminSite

from .models import TimeStampQApp
from .models import Questions


class MyAdminSite(AdminSite):
    site_header = 'Monty Python administration'

admin_site = MyAdminSite(name='myadmin')

admin_site.register(TimeStampQApp)
admin_site.register(Questions)
