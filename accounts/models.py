from django.contrib.auth.models import AbstractUser
from django.db import models


def user_directory_path(instance, filename):
    return "profile/{0}/{1}".format(instance.username, filename)


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(max_length=200, default="profile.png", upload_to=user_directory_path)
    