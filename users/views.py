from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse


def registration(request):
    if not request.user.is_authenticated:
        error = ''
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if username and email and password1 and password2:
                if password1 == password2:
                    try:
                        new_user = User.objects.create_user(username, email, password1)
                        login(request, new_user)
                        return HttpResponseRedirect(reverse(profile))
                    except IntegrityError:
                        error = 'User with this username exists please provide another name'
                else:
                    error = 'Passwords must be equals'
            else:
                error = 'All fields are required'
        return render(request, 'users/reg.html', {'error': error})
    else:
        return HttpResponseRedirect(reverse(profile))


def profile(request):
    error = ''
    if request.user.is_authenticated:
        user = get_object_or_404(User, username=request.user.get_username())
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            if username and email:
                if user.username != username or user.email != email:
                    if user.username != username:
                        user.username = username
                    if user.email != email:
                        user.email = email
                    user.save()
                    return HttpResponseRedirect(request.path_info)
                else:
                    error = 'You did not change anything'
            else:
                error = "This fields can't be blank"
    else:
        return redirect('login')
    return render(request, 'users/prof.html', {'error': error})


def loginuser(request):
    error = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            error = 'incorrect login or password '
    return render(request, 'users/login.html', {'error': error})


def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse(loginuser))


def change_password(request):
    error = ''
    if request.method == 'POST':
        user = User.objects.get(username=request.user.get_username())
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        if new_password and current_password:
            correct_pass = user.check_password(current_password)
            if new_password != current_password:
                if correct_pass:
                    user.set_password(new_password)
                    user.save()
                    return redirect('profile')
                else:
                    error = 'Your current password is incorrect try again'
            else:
                error = 'You new password must be different than previous'
        else:
            error = 'All fields are required'

    return render(request, 'users/change_password.html', {'error': error})


def delete_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = User.objects.get(username=request.user.get_username())
            user.delete()
            return HttpResponseRedirect(reverse(registration))
        return render(request, 'users/del.html')
    else:
        redirect('login')

