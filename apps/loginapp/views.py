from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt

def index(request):
    if 'email' in request.session:
        return redirect('/success')
    else:
        return render(request, 'login.html')


def registration(request):
    if request.method == 'POST':
        pw_hash = bcrypt.hashpw(request.POST['registration_password'].encode(), bcrypt.gensalt())
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            new_user = User.objects.create(first_name=request.POST['registration_first_name'], last_name=request.POST['registration_last_name'],email=request.POST['registration_email'], password=pw_hash)
            request.session['email'] = new_user.email
            request.session['first_name'] = new_user.first_name
            request.session['last_name'] = new_user.last_name
            print(new_user)
            return redirect('/success')

def login(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST['login_email'])
        except:
            messages.error(request, "E-mail address or password invalid")
            return redirect('/')
        if bcrypt.checkpw(request.POST['login_password'].encode(), user.password.encode()):
            request.session['email'] = user.email
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            return redirect('/success')
        else:
            messages.error(request, "E-mail address or password invalid")
            return redirect('/')
    if 'email' not in request.session:
        return redirect('/')


def success(request):
    if 'email' not in request.session:
        return redirect('/')
    else:
        # messages.error(request, 'Successfully Logged In!')
        return redirect('/quotes')

def logout(request):
    if 'email' in request.session:
        try:
            del request.session['email']
        except:
            pass
    return redirect('/')