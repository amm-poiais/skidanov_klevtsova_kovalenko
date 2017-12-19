from django import forms


class UserLoginForm(forms.Form):
    login = forms.CharField(min_length=6)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)


class UserRegisterForm(forms.Form):
    login = forms.CharField(min_length=6)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput)
    confirm_password = forms.CharField(min_length=8, widget=forms.PasswordInput)