from django.db import models
import re, bcrypt
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData["email"])
        if not user:
            errors["login"] = "Account does not exist"
        else:
            if not bcrypt.checkpw(postData["password"].encode(), user[0].password.encode()):
                errors["password"] = "Invalid email or password"
        return errors
    def register_validator(self, postData):
        errors = {}
        if len(postData["username"]) < 2:
            errors["username"] = "Name must be at least 1 characters"
        if not email_regex.match(postData["email"]):
            errors["regex"] = "Invalid email format"
        user = User.objects.filter(email=postData["email"])
        if user:
            errors["duplicate"] = "An account with this email already exists"
        if len(postData["password"]) < 6:
            errors["password"] = "Password must be at least 6 characters"
        if postData["password"] != postData["password_conf"]:
            errors["password_conf"] = "Passwords must match"
        return errors

class User(models.Model):
    username = models.CharField(max_length=60)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class PostManager(models.Manager):
    def post_validator(self, postData):
        errors = {}
        if len(postData["content"]) < 2 or len(postData["content"]) > 140:
            errors["content"] = "Post must be between 2 and 140 characters"
        return errors

class Post(models.Model):
    content = models.CharField(max_length=140)
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    users_who_liked = models.ManyToManyField(User, related_name="liked_posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()

class Comment(models.Model):
    content = models.CharField(max_length=140)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)