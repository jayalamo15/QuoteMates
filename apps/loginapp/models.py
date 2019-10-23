from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['registration_first_name']) < 2:
            errors['registration_first_name'] = 'First name should be at least 2 characters'
        if len(postData['registration_last_name']) < 2:
            errors['registration_last_name'] = 'Last name should be at least 2 characters'
        if not EMAIL_REGEX.match(postData['registration_email']):
            errors['registration_email'] = "Must enter valid email address"
        if len(postData['registration_password']) < 8:
            errors['registration_password'] = 'Password must be at least 8 characters'
        if postData['registration_confirm_password'] != postData['registration_password']:
            errors['registration_confirm_password'] = "Password must match"
        try:
            user = User.objects.get(email=postData['registration_email'])
            errors['registration_email'] = 'Email address already taken'
        except:
            pass
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

