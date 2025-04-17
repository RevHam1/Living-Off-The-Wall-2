from django.contrib import messages
from django.shortcuts import redirect, render

from .models import *


# Root route, to display the Registration/Login page
def index(request):
    return render(request, "login/index.html")

# Register route, to create a user


def register(request):
    errors = User.objects.validator(request.POST, "registration")

    if len(errors) > 0:
        # If the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # Redirect the user back to the  reg/login page to fix the errors
        return redirect("/")
    else:
        User.objects.create(first_name=request.POST['reg-fname'], last_name=request.POST['reg-lname'],
                            email=request.POST['reg-email'], password=request.POST['reg-pword'])
        thisUser = User.objects.last()
        request.session['user_id'] = thisUser.id
        request.session['user_fname'] = thisUser.first_name
        return redirect("/wall")

# Login route, checks that the email/password combination entered matches a valid user in the database


def login(request):
    checkUser = User.objects.filter(
        email=request.POST['log-email'], password=request.POST['log-pword'])
    if (len(checkUser) < 1):
        # If there is no match, we return to the reg/login page with an error message, as stated below
        messages.error(
            request, "The email and password combination entered do not match a record in our database")
        return redirect("/")
    else:
        request.session['user_id'] = checkUser[0].id
        request.session['user_fname'] = checkUser[0].first_name
        return redirect("/wall")
