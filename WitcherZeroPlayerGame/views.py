from sqlite3 import Date

from django.shortcuts import render, redirect, render_to_response
from WitcherZeroPlayerGame import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import JsonResponse
from WitcherZeroPlayerGame import models
from WitcherZeroPlayerGame.management.commands import generateevent

from datetime import date, datetime
from random import randint

from WitcherZeroPlayerGame.management.commands import generateevent
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
        #if form.is_valid() and User.objects.get(username=form.cleaned_data['login'], password=form.cleaned_data['password']):
            user2 = User.objects.get_by_natural_key(username)
            user2.profile.last_seen = datetime.now()
            auth.login(request, user2)
            if user2.profile.witcher is None:
                return redirect('/create_witcher/')
            else:
                return redirect('/home/')
            #return render(request, 'create_witcher.html')
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
            user.profile.last_seen = datetime.now()
            user.save()
            auth.authenticate(username=user.username, password=form.cleaned_data['password'])
            auth.login(request, user)
            return redirect('/create_witcher/')
        else:
            return redirect('/register/')
    else:
        form = forms.UserRegisterForm()
        return render(request, 'register.html', {'form': form, })

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
    request.user.profile.last_seen = datetime.now()
    request.user.save()
    if request.user.profile.witcher is not None:
        events = []
        for event in models.WitcherEvent.objects.filter(witcher=request.user.profile.witcher).order_by('-date')[:10]:
            events.append({'date': event.date.strftime('%d.%m.%y %H:%M:%S'), 'message': event.event})
        events.reverse()
        friends = []
        # generateevent.Command.generate_meeting_event(request.user)
        for friend in models.WitchersRelationship.objects.filter(first_witcher=request.user.profile.witcher):
            friends.append({'friend': friend.second_witcher.name, 'relation': friend.relationship.name})
        return render(request, 'home.html', {'events': events, 'friends': friends})
    else:
        return redirect('/create_witcher/')


@login_required(login_url='/login/')
def get_events(request):
    events = []
    for event in models.WitcherEvent.objects.filter(witcher=request.user.profile.witcher).order_by('-date')[:10]:
        events.append({'date': event.date.strftime('%d.%m.%y %H:%M:%S'), 'message': event.event})
    events.reverse()
    request.user.profile.last_seen = datetime.now()
    request.user.save()
    data = {
        'events': events,
    }
    return JsonResponse(data)


@login_required(login_url='/login/')
def get_friends(request):
    # generateevent.Command.generate_meeting_event(request.user)
    friends = []
    for friend in models.WitchersRelationship.objects.filter(first_witcher=request.user.profile.witcher):
        friends.append({'friend': friend.second_witcher.name, 'relation': friend.relationship.name})
    request.user.profile.last_seen = datetime.now()
    request.user.save()
    data = {'friends': friends}
    return JsonResponse(data)


@login_required(login_url='/login/')
def generate_positive_event(request):
    if request.user.profile.possible_positive_events > 0:
        request.user.profile.possible_positive_events -= 1
        generateevent.Command.generate_positive_event(request.user)
        request.user.save()
        event = models.WitcherEvent.objects.filter(witcher=request.user.profile.witcher).order_by('date').last()
        return JsonResponse(
            {'event': {'date': event.date.strftime('%d.%m.%y %H:%M:%S'), 'message': event.event}})
    else:
        return JsonResponse({'error': 'Вы уже потратили лимит событий!'})


@login_required(login_url='/login/')
def generate_negative_event(request):
    if request.user.profile.possible_negative_events > 0:
        request.user.profile.possible_negative_events -= 1
        generateevent.Command.generate_negative_event(request.user)
        request.user.save()
        event = models.WitcherEvent.objects.filter(witcher=request.user.profile.witcher).order_by('date').last()
        return JsonResponse(
            {'event': {'date': event.date.strftime('%d.%m.%y %H:%M:%S'), 'message': event.event}})
    else:
        return JsonResponse({'error': 'Вы уже потратили лимит событий!'})


@login_required(login_url='/login/')
def generate_random_event(request):
    event_type = randint(0, 1)
    if request.user.profile.possible_neutral_events > 0:
        request.user.profile.possible_neutral_events -= 1
        if event_type == 0:
            generateevent.Command.generate_negative_event(request.user)
        else:
            generateevent.Command.generate_positive_event(request.user)
        request.user.save()
        event = models.WitcherEvent.objects.filter(witcher=request.user.profile.witcher).order_by('date').last()
        return JsonResponse(
            {'event': {'date': event.date.strftime('%d.%m.%y %H:%M:%S'), 'message': event.event}})
    else:
        return JsonResponse({'error': 'Вы уже потратили лимит событий!'})
