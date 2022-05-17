from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse


def registration(request):
    error = ''
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if username and email and password1 and password2:
            if password1 == password2:
                # new_user = User.objects.create_user(username, email, password1)
                # return HttpResponseRedirect(reverse(profile, kwargs={'user_id': request.user.id}))
                try:
                    new_user = User.objects.create_user(username, email, password1)
                    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': request.user.id}))
                except Exception:
                    error = 'It Is an error occured'
            else:
                error = 'Passwords must be equals'
        else:
            error = 'All fields are required'
    return render(request, 'users/reg.html', {'error': error})


def profile(request, user_id):
    error = ''
    user = get_object_or_404(User, pk=user_id)
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
    return render(request, 'users/prof.html', {'error': error})
