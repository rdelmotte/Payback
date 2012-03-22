from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class UserProfile(models.Model):
    user    = models.ForeignKey(User, unique=True)
    tel     = models.CharField(max_length=100, blank=True)
    #friends         = models.ManyToManyField('self', blank=True)

    #def get_absolute_url(self):
    #    return ('profiles_profile_detail', (), { 'username': self.user.username })

    #get_absolute_url = models.permalink(get_absolute_url)


admin.site.register(UserProfile)