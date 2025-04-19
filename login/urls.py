from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),

    ## Wall FUNCTIONALITY ##
    path('create_message', views.create_mess),

    path('create_comment', views.create_comm),

    # path('user/<int:user_id>', views.profile),
    path('user/<int:user_id>/', views.profile, name='user_profile'),
    # path('like/<int:id>', views.add_like),
    path('delete/<int:mess_id>', views.delete_mess),
    path('comm_delete/<int:comm_id>', views.delete_comm),

    # Likes and unlikes
    path('like/<int:message_id>/', views.like_message, name='like_message'),
    path('unlike/<int:message_id>/', views.unlike_message, name='unlike_message'),
]
