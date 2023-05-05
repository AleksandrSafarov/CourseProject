from django.urls import path

from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('theme/<int:theme_id>', theme, name='theme')
]