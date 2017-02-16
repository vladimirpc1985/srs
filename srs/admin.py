from django.contrib import admin
from .models import Notefile, Notecard, Directory

admin.site.register(Notefile)
admin.site.register(Notecard)
admin.site.register(Directory)
