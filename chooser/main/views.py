import json

from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from .models import *

from .forms import *


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        themes = list(Theme.objects.all())
        themes.sort(key=lambda x: x.date, reverse=True)
        self.extra_context = {
            'themes': themes
        }
        return super().get_context_data(**kwargs)
        
    def get_success_url(self):
        return reverse_lazy('index')

def theme(request, theme_id):
    theme = Theme.objects.filter(id=theme_id)
    votesFor = list(VoteFor.objects.filter(theme=theme_id))
    votesAgainst = list(VoteAgainst.objects.filter(theme=theme_id))
    if len(votesAgainst) + len(votesFor) == 0:
        percent = -1
    elif int(len(votesFor) / (len(votesFor) + len(votesAgainst)) * 100) == len(votesFor) / (len(votesFor) + len(votesAgainst)) * 100:
        percent = round(len(votesFor) / (len(votesFor) + len(votesAgainst)) * 100)
    else:
        percent = len(votesFor) / (len(votesFor) + len(votesAgainst)) * 100
        percent = round(percent, 2)

    if len(theme) == 0:
        raise Http404
    
    context={
        'theme':theme[0],
        'votesFor':len(votesFor),
        'votesAgainst': len(votesAgainst),
        'percent': percent
    }

    return render(request, 'theme.html', context=context)

class CreateTheme(LoginRequiredMixin, CreateView):
    form_class = CreateThemeForm
    template_name = 'form.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Создать тему'
        context["button_text"] = "Создать"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect('index')

    
class PersonalArea(LoginRequiredMixin, TemplateView):
    template_name='personal.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        user_themes = list(Theme.objects.filter(user=self.request.user))
        user_themes.sort(key=lambda x: x.date, reverse=True)
        print(user_themes)
        self.extra_context = {
            'userthemes': user_themes
        }
        return super().get_context_data(**kwargs)