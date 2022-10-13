from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('new', views.new),
    path('login', views.login),
    path('register', views.register),
    path('forum', views.forum),
    path('logout', views.logout),
    path('post', views.post),
    path('<int:post_id>/comment', views.comment),
    path('<int:post_id>/delete', views.delete),
    path('<int:post_id>/like', views.like),
    path('<int:post_id>/unlike', views.unlike),
]