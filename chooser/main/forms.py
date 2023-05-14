from django import forms
from django.contrib.auth.forms import *
from django.contrib.auth.models import User
from .models import Theme
from django.forms import ModelForm


class CreateThemeForm(ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "Заголовок"})
        )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': "Описание"})
        )
    class Meta:
        model = Theme
        fields = ('title', 'description')