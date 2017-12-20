from django import forms
from WitcherZeroPlayerGame import models

class UserLoginForm(forms.Form):
    login = forms.CharField(min_length=6)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)


class UserRegisterForm(forms.Form):
    login = forms.CharField(min_length=6)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)
    confirm_password = forms.CharField(min_length=8, widget=forms.PasswordInput)


class CreateWitcherForm(forms.Form):
    name = forms.CharField(max_length=40)
    age = forms.IntegerField()
    school = forms.ModelChoiceField(queryset=models.WitcherSchool.objects.all().values_list('name'))

