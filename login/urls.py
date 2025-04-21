from django.urls import path

from . import views

urlpatterns = [
    # Register/Login
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    ## Wall FUNCTIONALITY ##
    path('wall/', views.wall, name='wall'),  # ✅ Updated route
    path('create_message', views.create_mess),
    path('create_comment', views.create_comm),
    path('user/<int:user_id>/', views.profile, name='user_profile'),
    path("blog/<int:post_id>/", views.blog_details, name="blog_details"),



    # Delete functionalities
    path('delete/<int:mess_id>', views.delete_mess),
    path('comm_delete/<int:comm_id>', views.delete_comm),

    path("delete_mess_confirm/<int:mess_id>/",
         views.delete_mess_confirm, name="delete_mess_confirm"),
    path("delete_comm_confirm/<int:comm_id>/",
         views.delete_comm_confirm, name="delete_comm_confirm"),

    # Likes and unlikes
    path('like/<int:message_id>/', views.like_message, name='like_message'),
    path('unlike/<int:message_id>/', views.unlike_message, name='unlike_message'),
]
