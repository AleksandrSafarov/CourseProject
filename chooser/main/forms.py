from django import forms
from django.contrib.auth.forms import *
from django.contrib.auth.models import User
from .models import Voting
from django.forms import ModelForm


class CreateVotingForm(ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Заголовок"})
        )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': "Описание"})
        )
    class Meta:
        model = Voting
        fields = ('title', 'description')