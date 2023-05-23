from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import *

from .models import *
from .forms import *
from .utils import StaffRequiredMixin


def getVote(request):
    if(request.GET.get('btnFor')):
        tId = int(request.GET.get('btnFor'))
        choosedTheme = Theme.objects.filter(id=tId)[0]
        if len(VoteFor.objects.filter(user=request.user, theme=choosedTheme)) or len(VoteAgainst.objects.filter(user=request.user, theme=choosedTheme)):
            return HttpResponseRedirect('/theme/%i'%int(request.GET.get('btnFor'))) 
        vote = VoteFor(user=request.user, theme=choosedTheme)
        vote.save()
        return HttpResponseRedirect('/theme/%i'%int(request.GET.get('btnFor')))
    elif(request.GET.get('btnAgainst')):
        tId = int(request.GET.get('btnAgainst'))
        choosedTheme = Theme.objects.filter(id=tId)[0]
        if len(VoteAgainst.objects.filter(user=request.user, theme=choosedTheme)) or len(VoteFor.objects.filter(user=request.user, theme=choosedTheme)):
            return HttpResponseRedirect('/theme/%i'%int(request.GET.get('btnAgainst'))) 
        vote = VoteAgainst(user=request.user, theme=choosedTheme)
        vote.save()
        return HttpResponseRedirect('/theme/%i'%int(request.GET.get('btnAgainst')))
    return render(request, 'index.html')

def deleteTheme(request):
    if request.GET.get('btnDel'):
        tId = int(request.GET.get('btnDel'))
        choosedTheme = Theme.objects.filter(id=tId)
        if len(choosedTheme) == 0:
            return HttpResponseRedirect('/del')
        choosedTheme.delete()
        return HttpResponseRedirect('/del')
    return render(request, 'index.html')
    

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

    if len(theme) == 0:
        raise Http404
    
    votesFor = list(VoteFor.objects.filter(theme=theme_id))
    votesAgainst = list(VoteAgainst.objects.filter(theme=theme_id))
    if len(votesAgainst) + len(votesFor) == 0:
        percent = -1
    elif int(len(votesFor) / (len(votesFor) + len(votesAgainst)) * 100) == len(votesFor) / (len(votesFor) + len(votesAgainst)) * 100:
        percent = round(len(votesFor) / (len(votesFor) + len(votesAgainst)) * 100)
    else:
        percent = len(votesFor) / (len(votesFor) + len(votesAgainst)) * 100
        percent = round(percent, 2)

    userVoteFor = []
    userVoteAgainst = []

    if request.user.is_authenticated:
        userVoteFor = VoteFor.objects.filter(theme=theme_id, user=request.user)
        userVoteAgainst = VoteAgainst.objects.filter(theme=theme_id, user=request.user)
    
    isVoted = False

    if len(userVoteFor) != 0 or len(userVoteAgainst) != 0:
        isVoted = True
    print(len(userVoteFor), len(userVoteAgainst))
    print(isVoted)
    
    context={
        'theme':theme[0],
        'votesFor':len(votesFor),
        'votesAgainst': len(votesAgainst),
        'percent': percent,
        'isVoted': isVoted
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
        self.extra_context = {
            'userthemes': user_themes
        }
        return super().get_context_data(**kwargs)

class DeleteThemes(StaffRequiredMixin, TemplateView):
    template_name = 'deleteThemes.html'
    login_url = 'login'
    def get_context_data(self, *, object_list=None, **kwargs):
        themes = Theme.objects.exclude(user=self.request.user)
        self.extra_context = {
            'themes': themes
        }
        return super().get_context_data(**kwargs)