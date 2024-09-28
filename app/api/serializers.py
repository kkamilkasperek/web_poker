from rest_framework.serializers import ModelSerializer, SerializerMethodField
from app.models import Blog, Message


class BlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"


class MessageSerializer(ModelSerializer):
    sender = SerializerMethodField()

    class Meta:
        model = Message
        fields = "__all__"
        extra_fields = ["sender"]

    def get_sender(self, obj):
        return obj.sender.username
