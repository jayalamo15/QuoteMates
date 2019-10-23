from __future__ import unicode_literals
from django.db import models
from apps.loginapp.models import User


class QuoteManager(models.Manager):
    def quote_validator(self, postData):
        errors = {}
        if len(postData['author']) <=2:
            errors['author'] = 'Author name must have at least 3 characters.'
        if len(postData['quote']) <=10:
            errors['quote'] = 'Quote must have at least 10 characters.'
        return errors

class Quote(models.Model):
    author = models.CharField(max_length = 50)
    quote = models.TextField()
    creator = models.ForeignKey(User, related_name = 'post')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
    users_who_like = models.ManyToManyField(User, related_name = 'liked_quotes')
    
