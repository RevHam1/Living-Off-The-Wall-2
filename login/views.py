from mailbox import Message

import bcrypt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Comment, User, Wall_Message


# Root route, to display the Registration/Login page
def index(request):
    return render(request, "login/index.html")

# def index(request):
#     return redirect("/wall/")


## Register, Login, Logout FUNCTIONALITIES ##
def register(request):
    if request.method == "POST":
        errors = User.objects.create_validator(request.POST)
        if errors:
            for value in errors.values():
                messages.error(request, value)
            return redirect('/')
        else:
            hashed_pw = bcrypt.hashpw(
                request.POST['password'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                birthday=request.POST['birthday'],
                password=hashed_pw
            )
            request.session['user_id'] = user.id
            return redirect('/wall')  # ✅ Updated redirect
    return redirect('/')


def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user:
            user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/wall')  # ✅ Updated redirect
        messages.error(request, "Email or password is incorrect")
    return redirect('/')


def logout(request):
    request.session.flush()
    # request.session.clear()
    return redirect('/wall')


## Wall CONTEXT ##
def wall(request):
    context = {
        # ✅ Show posts to everyone
        "all_messages": Wall_Message.objects.order_by("-created_at")
    }

    # ✅ If logged in, show user details
    if "user_id" in request.session:
        context["user"] = User.objects.get(id=request.session["user_id"])

    return render(request, "login/wall.html", context)

# profile post


def profile(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, "login/profile.html", {"user": user})


def blog_details(request, post_id):
    post = get_object_or_404(Wall_Message, id=post_id)
    # ✅ Retrieves all comments related to the post
    comments = Comment.objects.filter(wall_message=post)
    likes_count = post.user_likes.count()  # ✅ Counts the number of likes

    context = {
        "post": post,
        "comments": comments,
        "likes_count": likes_count
    }
    return render(request, "login/blog_details.html", context)


# CREATE Post, Comment-Integrate the ability to Post a message or comment on someone else’s message
# @login_required
# def create_mess(request):
#     if request.method == "POST":
#         new_mess = Wall_Message.objects.create(
#             content=request.POST["content"],
#             poster=User.objects.get(id=request.session["user_id"])
#         )
#         return redirect("/wall")
#     return redirect("/wall")
def create_mess(request):
    if "user_id" not in request.session:
        return redirect('/')

    if request.method == "POST":
        Wall_Message.objects.create(
            content=request.POST["content"],
            poster=User.objects.get(id=request.session["user_id"])
        )
    return redirect("/wall")


# @login_required
# def create_comm(request):
#     if request.method == "POST":
#         Comment.objects.create(
#             content=request.POST["content"],
#             poster=User.objects.get(id=request.session["user_id"]),
#             wall_message=Wall_Message.objects.get(id=request.POST["message"]),
#         )
#         return redirect("/wall")
#     return redirect("/wall")
def create_comm(request):
    if "user_id" not in request.session:
        return redirect('/')

    if request.method == "POST":
        Comment.objects.create(
            content=request.POST["content"],
            poster=User.objects.get(id=request.session["user_id"]),
            wall_message=Wall_Message.objects.get(id=request.POST["message"]),
        )
    return redirect("/wall")


# Like Unlike POST
# @login_required
# def like_message(request, message_id):
#     user = User.objects.get(id=request.session["user_id"])
#     message = Wall_Message.objects.get(id=message_id)
#     message.user_likes.add(user)
#     return redirect("/wall")

def like_message(request, message_id):
    if "user_id" not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session["user_id"])
    message = Wall_Message.objects.get(id=message_id)
    message.user_likes.add(user)
    return redirect("/wall")


# @login_required
# def unlike_message(request, message_id):
#     user = User.objects.get(id=request.session["user_id"])
#     message = Wall_Message.objects.get(id=message_id)
#     message.user_likes.remove(user)
#     return redirect("/wall")
def unlike_message(request, message_id):
    if "user_id" not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session["user_id"])
    message = Wall_Message.objects.get(id=message_id)
    message.user_likes.remove(user)
    return redirect("/wall")


# DELETE POST, COMMENT Implementatioin - delete functionality allowing users to delete only their own messages
def delete_mess(request, mess_id):
    if "user_id" not in request.session:
        return redirect('/')
    get_object_or_404(Wall_Message, id=mess_id).delete()
    return redirect('/wall')


def delete_comm(request, comm_id):
    if "user_id" not in request.session:
        return redirect('/')
    get_object_or_404(Comment, id=comm_id).delete()
    return redirect('/wall')


def delete_mess_confirm(request, mess_id):
    if "user_id" not in request.session:
        return redirect('/')
    message = get_object_or_404(Wall_Message, id=mess_id)
    if request.method == "POST":
        message.delete()
        return redirect('/wall')
    return render(request, "login/delete_confirm.html", {
        "message": message
    })


def delete_comm_confirm(request, comm_id):
    if "user_id" not in request.session:
        return redirect('/')
    comment = get_object_or_404(Comment, id=comm_id)
    if request.method == "POST":
        comment.delete()
        return redirect('/wall')
    return render(request, "login/delete_confirm.html", {
        "comment": comment
    })


# def delete_mess(request, mess_id):
#     Wall_Message.objects.get(id=mess_id).delete()
#     return redirect('/wall')


# def delete_comm(request, comm_id):
#     Comment.objects.get(id=comm_id).delete()
#     return redirect('/wall')


# # DELETE POST, COMMENT Confirmation
# def delete_mess_confirm(request, mess_id):
#     message = get_object_or_404(Message, id=mess_id)
#     if request.method == "POST":
#         message.delete()
#         return redirect("wall")
#     return render(request, "login/delete_confirm.html", {
#         "message": message,
#         "user": request.user
#     })


# def delete_comm_confirm(request, comm_id):
#     comment = get_object_or_404(Comment, id=comm_id)
#     if request.method == "POST":
#         comment.delete()
#         return redirect("wall")
#     return render(request, "login/delete_confirm.html", {
#         "comment": comment,
#         "user": request.user
#     })
