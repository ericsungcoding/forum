from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, "index.html")

def new(request):
    return render(request, "new.html")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if errors:
        for val in errors.values():
            messages.error(request, val)
        return redirect("/")
    user = User.objects.get(email=request.POST["email"])
    request.session["user_id"] = user.id
    return redirect("/forum")

def register(request):
    errors = User.objects.register_validator(request.POST)
    if errors:
        for val in errors.values():
            messages.error(request, val)
        return redirect("/new")
    user = User.objects.create(
        username = request.POST["username"],
        email = request.POST["email"],
        password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
    )
    request.session["user_id"] = user.id
    return redirect("/forum")

def forum(request):
    context = {
        "user": User.objects.get(id=request.session["user_id"]),
        "all_posts": Post.objects.all()
    }
    return render(request, "forum.html", context)

def logout(request):
    request.session.flush()
    return redirect("/")

def post(request):
    errors = Post.objects.post_validator(request.POST)
    if errors:
        for val in errors.values():
            messages.error(request, val)
        return redirect("/forum")
    Post.objects.create(
        content = request.POST["content"],
        user = User.objects.get(id=request.session["user_id"])
    )
    return redirect("/forum")

def comment(request, post_id):
    Comment.objects.create(
        content = request.POST["content"],
        user = User.objects.get(id=request.session["user_id"]),
        post = Post.objects.get(id=post_id)
    )
    return redirect("/forum")

def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect("/forum")

def like(request, post_id):
    user = User.objects.get(id=request.session["user_id"])
    post = Post.objects.get(id=post_id)
    post.users_who_liked.add(user)
    return redirect("/forum")

def unlike(request, post_id):
    user = User.objects.get(id=request.session["user_id"])
    post = Post.objects.get(id=post_id)
    post.users_who_liked.remove(user)
    return redirect("/forum")