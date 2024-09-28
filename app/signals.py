from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
from .models import RoomUser

#___________SIGNALS____________________

@receiver(post_delete, sender=RoomUser)
def delete_empty_room(sender, instance, **kwargs):
    room = instance.room
    if room.participants.count() == 0:
        room.delete()

@receiver(post_save, sender=RoomUser)
def room_exists(sender, instance, created,  **kwargs):
    room = instance.room
    if created:
        room.save()

@receiver(user_logged_out)
def remove_user_from_rooms(sender, request, user, **kwargs):
    RoomUser.objects.filter(user=user).delete()

#___________END OF SIGNALS____________________