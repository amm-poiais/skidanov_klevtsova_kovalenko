from django.shortcuts import render, redirect
from WitcherZeroPlayerGame import forms

# Create your views here.


def login(request):
    if request.method == 'POST':
        form = forms.UserLoginForm(request.POST)
        if form.is_valid():
            return render(request, 'hello_world.html', {'message': 'Hello everyone!', })
        else:
            return render(request, 'login.html', {'form': form, })
    else:
        form = forms.UserLoginForm()
        return render(request, 'login.html', {'form': form, })


def register(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            return redirect('/create_witcher/')
        else:
            return redirect('/register/')
    else:
        form = forms.UserRegisterForm()
        return render(request, 'register.html', {'form': form, })
