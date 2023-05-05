import json

from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from .models import *


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        self.extra_context = {
            'themes': Theme.objects.all()
        }
        return super().get_context_data(**kwargs)
        
    def get_success_url(self):
        return reverse_lazy('index')

def theme(request, theme_id):
    theme = Theme.objects.filter(id=theme_id)
    votesFor = VoteFor.objects.filter(theme=theme_id)
    votesAgainst = VoteAgainst.objects.filter(theme=theme_id)
    
    if len(theme) == 0:
        raise Http404
    
    context={
        'theme':theme[0],
    }

    return render(request, 'theme.html', context=context)