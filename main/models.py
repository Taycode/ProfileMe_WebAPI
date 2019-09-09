from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    github = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    behance = models.CharField(max_length=100, blank=True)
    dribble = models.CharField(max_length=100, blank=True)
    linkedin = models.CharField(max_length=100, blank=True)
    about_me = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.user.username


def create_user_profile(sender, **kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_user_profile, User)
