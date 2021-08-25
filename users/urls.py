from django.urls import path

from django.contrib.auth import views as auth_views
from .views import home_view, signup_view, profile, user_logout, update, UserDelete, LoginView, activate

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('', home_view, name='blog-home'),
    path('signup/', signup_view, name='signup'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('logout/', user_logout, name='logout'),

    path('profile/', profile, name='profile'),
    path('update/', update, name='update'),
    path('user_delete/<int:pk>/', UserDelete.as_view(), name='user_delete'),
]