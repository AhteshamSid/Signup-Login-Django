from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)


CustomUser._meta.get_field('email')._unique = True


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=CustomUser)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
