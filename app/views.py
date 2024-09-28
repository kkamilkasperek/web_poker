from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from .forms import BlogForm, RegisterForm, ProfileForm, PokerForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Blog, PrivateChat, Message, PublicChat, PokerRoom, RoomUser
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages




# blogs_list = [
#     {"id": 1, "title": "Blog 1", "content": "This is the content of blog 1"},
#     {"id": 2, "title": "Blog 2", "content": "This is the content of blog 2"},
#     {"id": 3, "title": "Blog 3", "content": "This is the content of blog 3"}
# ]

def index(request):
    return render(request, "app/index.html")


def blogs(request):
    blogs_list = Blog.objects.all()
    context = {"blogs": blogs_list}
    return render(request, "app/blogs.html", context)


def blog(request, pk):
    context = {"blog": Blog.objects.get(id=pk)}
    return render(request, "app/blog.html", context)


@login_required(login_url="login")
def create_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect("blogs")
    else:
        form = BlogForm()
        context = {"form": form}
        return render(request, "app/blog_form.html", context)


def edit_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    form = BlogForm(instance=blog)
    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect("blogs")
    context = {"form": form}
    return render(request, "app/blog_form.html", context)


def delete_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.method == "POST":
        blog.delete()
        return redirect("blogs")
    context = {"blog": blog}
    return render(request, "app/delete.html", context)


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect("index")
    else:
        form = AuthenticationForm()
    context = {"form": form, "type": "login"}
    return render(request, "app/login_register.html", context)


def user_register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = RegisterForm()
    context = {"form": form, "type": "register"}
    return render(request, "app/login_register.html", context)


def user_logout(request):
    logout(request)
    return redirect("index")


def profile(request, pk):
    query_user = User.objects.get(id=pk)
    context = {"query_user": query_user}
    return render(request, "app/user_profile.html", context)


@login_required(login_url="login")
def edit_profile(request):
    if request.method == "POST":
        form_profile = ProfileForm(request.POST, instance=request.user)
        form_password = PasswordChangeForm(request.user, data=request.POST)
        if form_profile.is_valid() and form_password.is_valid():
            form_profile.save()
            form_password.save()
            update_session_auth_hash(request, request.user)
            return redirect("profile")
    else:
        form_profile = ProfileForm(instance=request.user)
        form_password = PasswordChangeForm(request.user)
    context = {"form_profile": form_profile, "form_password": form_password}
    return render(request, "app/user_profile_form.html", context)

@login_required(login_url="login")
def private_chat(request, pk):
    receiver = User.objects.get(id=pk)
    if request.method == "POST":
        message = request.POST.get("message")
        chat = PrivateChat.objects.filter(
            Q(user1=request.user, user2=receiver) | Q(user1=receiver, user2=request.user)
        ).first()
        if not chat:
            chat = PrivateChat.objects.create(user1=request.user, user2=receiver)
        Message.objects.create(chat=chat, sender=request.user, message=message)
        return HttpResponseRedirect(request.path_info)
    else:
        chat = PrivateChat.objects.filter(
            Q(user1=request.user, user2=receiver) | Q(user1=receiver, user2=request.user)
        ).first()
        if not chat:
            chat = None
        return render(request, "app/private_chat.html", {"chat": chat, "receiver": receiver})

@login_required(login_url="login")
def my_chats(request):
    chats = PrivateChat.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    return render(request, "app/my_chats.html", {"chats": chats})

@login_required(login_url="login")
def public_chat(request):
    publicChat = PublicChat.objects.get_or_create(id=1)
    messages = Message.objects.filter(public_chat=publicChat[0])
    return render(request, "app/public_chat.html", {"messages": messages})

def poker_rooms(request):
    rooms = PokerRoom.objects.all()
    return render(request, "app/poker_rooms.html", {"rooms": rooms})

@login_required(login_url="login")
def create_poker(request):
    if request.method == "POST":
        form = PokerForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            if not room.is_private:
                room.password = None
            room.save()
            #room.participants.add(request.user)
            RoomUser.objects.create(user=request.user, room=room, position=1)
            return redirect("poker-room", pk=room.id)
    form = PokerForm()
    return render(request, "app/poker_room_form.html", {"form": form})


def poker_room(request, pk):
    room = PokerRoom.objects.get(id=pk)
    participants = RoomUser.objects.filter(room=room)
    is_participant = request.user in room.participants.all()
    positions = list(range(1, 9))
    context = {"room": room, "participants": participants, "is_participant": is_participant, "positions": positions}
    return render(request, "app/poker_room.html", context)

@login_required(login_url="login")
def join_poker(request, pk):
    room = PokerRoom.objects.get(id=pk)
    if room.participants.count() >= 8:
        messages.error(request, "Room is full")
        return redirect("poker-room", pk=pk)

    occupied_positions = RoomUser.objects.filter(room=room).values_list("position", flat=True)
    for position in range(1, 9):
        if position not in occupied_positions:
            RoomUser.objects.create(user=request.user, room=room, position=position)
            break

    #RoomUser.objects.create(user=request.user, room=room)
    return redirect("poker-room", pk=pk)

@login_required(login_url="login")
def leave_poker(request, pk):
    room = PokerRoom.objects.get(id=pk)
    RoomUser.objects.filter(user=request.user, room=room).delete()
    if room.participants.count():
        return redirect("poker-room", pk=pk)
    else:
        return redirect("poker-rooms")

@login_required(login_url="login")
def remove_user_from_rooms(request):
    RoomUser.objects.filter(user=request.user).delete()
    return JsonResponse({"status": "ok"})