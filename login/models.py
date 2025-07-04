import re
from datetime import datetime

from django.db import models

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def create_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 1:
            errors['first_name'] = "First name cannot be blank!"
        if len(postData['last_name']) < 1:
            errors['last_name'] = "Last name cannot be blank!"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Passwords do not match."

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if User.objects.filter(email=postData['email']).exists():
            errors['email'] = "Duplicate, email already registed"

        # date = datetime.strptime(postData['birthday'],"%Y-%m-%d")
        # if date > datetime.now():
        #     errors['birthday'] = "Birthdate cannot be in the future"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    birthday = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Wall_Messa_Mang(models.Manager):
    def mess_validator(self, postData):
        errors = ""
        if len(postData['content']) < 1:
            errors = "Post a message must be at least two characters"
        return errors


class Wall_Message(models.Model):
    content = models.TextField()
    poster = models.ForeignKey(
        User, related_name='messages', on_delete=models.CASCADE)
    user_likes = models.ManyToManyField(User, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = Wall_Messa_Mang()

    def __str__(self):
        return self.content[:15] + ("..." if len(self.content) > 15 else "")


class Comment(models.Model):
    content = models.CharField(max_length=140)
    poster = models.ForeignKey(
        User, related_name='user_comments', on_delete=models.CASCADE)
    wall_message = models.ForeignKey(
        Wall_Message, related_name="post_comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:15] + ("..." if len(self.content) > 15 else "")
