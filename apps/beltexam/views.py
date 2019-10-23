from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Quote
from apps.loginapp.models import User
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def index(request):
    if 'email' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(email = request.session['email'])
        context = {
            'quotes': Quote.objects.all(),
            'user':user
        }
        return render(request, 'beltexam.html', context)

def new_quote(request):
    if request.method == 'POST':
        errors = Quote.objects.quote_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            new_quote = Quote.objects.create(author=request.POST['author'],quote=request.POST['quote'],creator=User.objects.get(first_name=request.session['first_name']))
            print(new_quote)
            messages.error(request, 'Your quote was posted!')
    else:
        pass
    return redirect('/')

def like_quote(request, quote_id):
    if request.method == 'POST':
        user = User.objects.get(email = request.session['email'])
        quote_to_like = Quote.objects.get(id=quote_id)
        if quote_to_like.users_who_like.add(user) == 1:
            return redirect('/')
        else:
            quote_to_like.users_who_like.add(user)
    return redirect('/')

def edit_account(request, user_id):
    context = {
        'users': User.objects.get(id=user_id)
    }
    return render(request, 'editaccount.html', context)

def update_account(request, user_id):
    if request.method == 'POST':
        update = User.objects.get(id=user_id)
        try:
            if request.POST['edit_email'] in request.session:
                pass
        except:
            user = User.objects.get(email=request.POST['edit_email'])
            messages.error(request, 'Email address already taken')
        
        if len(request.POST['edit_first_name']) == 0:
            messages.error(request, 'All fields must be filled')
            return redirect(f'/quotes/myaccount/{user_id}')
        if len(request.POST['edit_last_name']) == 0:
            messages.error(request, 'All fields must be filled')
            return redirect(f'/quotes/myaccount/{user_id}')
        if len(request.POST['edit_email']) == 0:
            messages.error(request, 'All fields must be filled')
            return redirect(f'/quotes/myaccount/{user_id}')
        if not EMAIL_REGEX.match(request.POST['edit_email']):
            messages.error(request, 'Enter valid email address')
            return redirect(f'/quotes/myaccount/{user_id}')
        else:
            update.first_name=request.POST['edit_first_name']
            update.last_name=request.POST['edit_last_name']
            request.session['first_name'] = request.POST['edit_first_name']
            request.session['last_name'] = request.POST['edit_last_name']
            try: 
                if request.POST['edit_email'] in request.session:
                    pass
            except:
                update.email=request.POST['edit_email']
            update.save()
            return redirect(f'/quotes/user/{user_id}')

def show_user(request, user_id):
    context = {
        'user': User.objects.get(id=user_id)
    }
    return render(request, 'showuser.html', context)

def delete(request, quote_id):
    if request.method == 'POST':
        quote = Quote.objects.get(id=quote_id)
        if quote.creator.email == request.session['email']:
            destroy = Quote.objects.get(id=quote_id)
            destroy.delete()
            return redirect('/')
        else:
            messages.error(request, 'Can only delete quotes you post')
            return redirect('/')
