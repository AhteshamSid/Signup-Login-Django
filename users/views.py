from django.contrib.auth import views as auth_views
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views import generic
from django.urls import reverse_lazy

from .forms import LoginForm  # RegisterForm
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

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model

UserModel = get_user_model()
from .tokens import account_activation_token


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
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            print(current_site)
            mail_subject = 'Activate your account.'
            message = render_to_string('account-active.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            print(message)
            # email_from = settings.EMAIL_HOST_USER
            to_email = form.cleaned_data.get('email')
            # recipient_list = [user.email, ]
            # send_mail(mail_subject, message, email_from, recipient_list)# email.send()
            msg = EmailMessage(mail_subject, message, to=[to_email])
            try:
                msg.send()
                messages.info(request, 'verify Your email!')
            except:
                messages.info(request, 'Your email wrong!')
            return redirect('blog-home')
        else:
            messages.error(request, 'Correct the errors below')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('blog-home')
    else:
        return HttpResponse('Activation link is invalid!')


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
    return render(request, 'home.html', )


class UserDelete(generic.DeleteView):
    model = CustomUser
    template_name = "user_delete.html"
    success_url = reverse_lazy('blog-home')
