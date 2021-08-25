from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django import forms
# from django.contrib.auth.models import User

from .models import Profile, CustomUser


class SignUpForm(UserCreationForm):
    address = forms.CharField(max_length=100, required=True,)
    email = forms.EmailField(max_length=254, required=True,)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'address', )


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Username')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address']
        labels = {'Address': 'Address'}