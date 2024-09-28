from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import BlogSerializer, MessageSerializer

from app.models import Blog, Message


@api_view(["GET"])
def get_routes(request):
    routes = [
        "GET /api",
        "GET /api/blogs",
        "GET /api/blogs/:id",
        "GET /api/chats/:id/messages?last_message_id=last",
    ]
    return Response(routes)

@api_view(["GET"])
def get_blogs(request):
    blogs = Blog.objects.all()
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    serializer = BlogSerializer(blog, many=False)
    return Response(serializer.data)

@api_view(["GET"])
def get_new_messages(request, chat_id):
    last_message_id = request.GET.get("last_message_id")
    if last_message_id:
        messages = Message.objects.filter(chat_id=chat_id, id__gt=last_message_id).order_by("timestamp")
    else:
        messages = Message.objects.filter(chat_id=chat_id).order_by("timestamp")
    # messages = Message.objects.filter(chat_id=chat_id).order_by("timestamp")

    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)