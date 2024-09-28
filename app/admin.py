from django.contrib import admin

# Register your models here.

from .models import Blog
from .models import PrivateChat
from .models import Message
from .models import PublicChat
from .models import PokerRoom
from .models import RoomUser

admin.site.register(Blog)
admin.site.register(PrivateChat)
admin.site.register(Message)
admin.site.register(PublicChat)
admin.site.register(RoomUser)
admin.site.register(PokerRoom)


