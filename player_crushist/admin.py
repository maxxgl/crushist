from django.contrib import admin

from .models import Song
from .models import Event
from .models import User

admin.site.register(Song)
admin.site.register(Event)
admin.site.register(User)
