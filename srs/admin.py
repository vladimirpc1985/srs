from django.contrib import admin
from .models import Post
from .models import Notefile
from .models import Notecard

admin.site.register(Post)
admin.site.register(Notefile)
admin.site.register(Notecard)
