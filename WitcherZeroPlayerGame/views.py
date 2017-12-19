from sqlite3 import Date

from django.shortcuts import render, redirect, render_to_response
from WitcherZeroPlayerGame import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth

from datetime import date, datetime

# Create your views here.


def login(request):
    if request.method == 'POST':
        form = forms.UserLoginForm(request.POST)
        username = request.POST['login']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
        #if form.is_valid() and User.objects.get(username=form.cleaned_data['login'], password=form.cleaned_data['password']):
            return render(request, 'create_witcher.html')
        else:
            return render(request, 'login.html', {'form': form, })
    else:
        form = forms.UserLoginForm()
        return render(request, 'login.html', {'form': form, })


def register(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['login'], 'email', form.cleaned_data['password'])
            user.profile.last_seen = datetime.today()
            user.save()
            return redirect('/create_witcher/')
        else:
            return redirect('/register/')
    else:
        form = forms.UserRegisterForm()
        return render(request, 'register.html', {'form': form, })


@login_required(login_url='/login/')
def create_witcher(request):
    if request.method == 'GET':
        return render(request, 'create_witcher.html')
    else:
        return redirect('/hello_world/')