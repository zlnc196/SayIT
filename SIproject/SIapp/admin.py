from django.contrib import admin
from .models import CustomUser, Posts

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Posts)