from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # login 
    path("", views.login_action, name='login'),
    path('logout', views.logout_action, name='logout'),
    path("register", views.register, name='register'),

    # viewing posts
    path('global', views.globalStream, name='global'),
    path('followers', views.followerStream, name='followers'),

    # profiles 
    path('myprofile/<int:id>', views.myProfile, name='myprofile'),
    path('otherprofile/<int:id>', views.otherProfile, name='otherprofile'),

    # actions
    path('follow/<int:id>', views.follow, name='follow'),
    path('unfollow/<int:id>', views.unfollow, name='unfollow'),
    path('picture/<int:id>', views.get_photo, name='picture'),

    # ajax
    path('get-global', views.globalStream_json_serializer, name='get-global'),
    path('get-follower', views.followerStream_json_serializer, name='get-follower'),
    path('add-comment', views.add_comment, name='add-comment'),

]

