from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

'''
Private Chat implemented using client side fetch API and rest API server side
'''
class PrivateChat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2")


    def __str__(self):
        return f"{self.user1.username} - {self.user2.username}"

class PublicChat(models.Model):
    def __str__(self):
        return "Public Chat"


class Message(models.Model):
    public_chat = models.ForeignKey(PublicChat, on_delete=models.CASCADE, null=True, blank=True)
    chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} : {self.message[:15]}"


class PokerRoom(models.Model):
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField(User, related_name="rooms", through="RoomUser")
    is_private = models.BooleanField(default=False)
    password = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class RoomUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(PokerRoom, on_delete=models.CASCADE)
    position = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} in {self.room.name}"
