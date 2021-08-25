from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy

from .forms import LoginForm # RegisterForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views import generic

from .models import Profile, CustomUser
from .forms import SignUpForm, ProfileUpdateForm, UserUpdateForm


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('login')


# class RegisterView(generic.CreateView):
#     form_class = RegisterForm
#     template_name = 'register.html'
#     success_url = reverse_lazy('login')

def signup_view(request):
    # if request.user.is_authenticated:
    #     return redirect('blog-home')
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.address = form.cleaned_data.get('address')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('blog-home')
        else:
            messages.error(request, 'Correct the errors below')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}

    return render(request, 'profileUpdate.html', context)


def user_logout(request):
    logout(request)
    return redirect('blog-home')

def home_view(request):
    user = CustomUser.objects.all()
    return render(request, 'home.html',)



class UserDelete(generic.DeleteView):
    model = CustomUser
    template_name = "user_delete.html"
    success_url = reverse_lazy('blog-home')
