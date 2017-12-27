from sqlite3 import Date

from django.shortcuts import render, redirect, render_to_response
from WitcherZeroPlayerGame import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from WitcherZeroPlayerGame import models

from datetime import date, datetime

# Create your views here.


def main(request):
    return redirect('/home/')


def login(request):
    if request.method == 'POST':
        form = forms.UserLoginForm(request.POST)
        username = request.POST['login']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if form.is_valid() and user is not None and user.is_active:
            user2 = User.objects.get_by_natural_key(username)
            user2.profile.last_seen = datetime.now()
            auth.login(request, user2)
            if user2.profile.witcher is None:
                return redirect('/create_witcher/')
            else:
                return redirect('/home/')
        else:
            return render(request, 'login.html', {'form': form, 'message': 'Неверный логин или пароль!'})
    else:
        form = forms.UserLoginForm()
        return render(request, 'login.html', {'form': form, 'message': ''})


def register(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['login']).count() != 0:
                return render(request, 'register.html', {'form': form, 'message': 'Такой логин занят!'})
            else:
                user = User.objects.create_user(form.cleaned_data['login'], 'email', form.cleaned_data['password'])
                user.profile.last_seen = datetime.now()
                user.save()
                auth.authenticate(username=user.username, password=form.cleaned_data['password'])
                auth.login(request, user)
                return redirect('/create_witcher/')
        else:
            return render(request, 'register.html', {'form': form, 'message': 'Неккоректные данные!'})
    else:
        form = forms.UserRegisterForm()
        return render(request, 'register.html', {'form': form, 'message': ''})


@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return redirect('/login/')


@login_required(login_url='/login/')
def create_witcher(request):
    if request.method == 'POST':
        form = forms.CreateWitcherForm(request.POST)
        if form.is_valid():
            witcher = models.Witcher(name=form.cleaned_data['name'], age=form.cleaned_data['age'], school=form.cleaned_data['school'], status='Жив')
            witcher.save()
            request.user.profile.witcher = witcher
            request.user.save()
            return redirect('/home/')
        else:
            return redirect('/create_witcher/')
    else:
        form = forms.CreateWitcherForm()
        return render(request, 'create_witcher.html', {'form': form, })


@login_required(login_url='/login/')
def home(request):
    if request.user.profile.witcher is not None:
        return render(request, 'home.html', {})
    else:
        return redirect('/create_witcher/')

