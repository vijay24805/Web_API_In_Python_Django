"""
to store chat and channels objects in database
"""
from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm


class HotList(models.Model):
    """
    saves top10 channels
    """
    Channel = models.CharField(max_length = 100)
    Description = models.CharField(default = True, null = True, \
    max_length = 100)
    Game = models.CharField(default = True, null = True, max_length = 100)
    viewers = models.IntegerField(default = True, max_length = 100)

class Chat(models.Model):
    """
    Chat app to store user comments
    """
    user = models.ForeignKey(User)
    userName = models.CharField(primary_key = True, max_length = 100)
    opinion = models.TextField(null= True, max_length = 3000)
    added = models.DateTimeField(auto_now_add = True)

class ChatForm(ModelForm):
    """
    creating ORM for chat app
    """
    opinion = forms.CharField(widget = forms.Textarea(attrs = \
    {'cols' : 120, 'rows' : 8}) )
    class Meta:
        """
        Meta
        """
        model = Chat
        exclude = {'user'}

