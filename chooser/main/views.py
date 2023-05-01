import json

from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from django.contrib.auth.models import User

class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        self.extra_context = {
        }
        return super().get_context_data(**kwargs)
        
    def get_success_url(self):
        return reverse_lazy('index')