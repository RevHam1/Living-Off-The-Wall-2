import bcrypt
from django.contrib import messages
from django.shortcuts import redirect, render

from .models import User, Wall_Message


# Root route, to display the Registration/Login page
def index(request):
    return render(request, "login/index.html")

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
            return redirect('/success')
    return redirect('/')


def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])
        if user:
            user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
                request.session['user_id'] = user.id
                return redirect('/success')
        messages.error(request, "Email or password is incorrect")
    return redirect('/')


def success(request):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or login!")
        return redirect('/')

    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'all_messages': Wall_Message.objects.order_by('-created_at'),
    }
    return render(request, "login/success.html", context)


def logout(request):
    request.session.flush()
    # request.session.clear()
    return redirect('/')


## Wall FUNCTIONALITY ##
# CREATE Post, Comment-Integrate the ability to Post a message or comment on someone else’s message
def create_mess(request):
    if request.method == 'POST':
        error = Wall_Message.objects.mess_validator(request.POST)
        if error:
            messages.error(request, error)
            return redirect('/success')
        new_mess = Wall_Message.objects.create(
            content=request.POST['content'],
            poster=User.objects.get(id=request.session['user_id'])
        )
        print(new_mess)
        return redirect('/success')
    return redirect('/')


# READ POST
def profile(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, "profile.html", context)


def like_message(request, message_id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or login!")
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    message = Wall_Message.objects.get(id=message_id)
    message.user_likes.add(user)
    return redirect('/success')


def unlike_message(request, message_id):
    if 'user_id' not in request.session:
        messages.error(request, "You need to register or login!")
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    message = Wall_Message.objects.get(id=message_id)
    message.user_likes.remove(user)
    return redirect('/success')


# # DELETE MESSAGE-Implement delete functionality allowing users to delete only their own messages
# def delete_mess(request, mess_id):
#     Wall_Message.objects.get(id=mess_id).delete()
#     return redirect('/success')


# def delete_comm(request, comm_id):
#     Comment.objects.get(id=comm_id).delete()
#     return redirect('/success')
