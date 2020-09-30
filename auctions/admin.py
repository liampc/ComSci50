from django.contrib import admin

# Register your models here.
from .models import User, Listing

admin.site.register(User)
admin.site.register(Listing)