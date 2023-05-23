from django.http import Http404, HttpResponseRedirect
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
        choosedVoting = Voting.objects.filter(id=tId)[0]
        if len(VoteFor.objects.filter(user=request.user, voting=choosedVoting)) or len(VoteAgainst.objects.filter(user=request.user, voting=choosedVoting)):
            return HttpResponseRedirect('/voting/%i'%int(request.GET.get('btnFor'))) 
        vote = VoteFor(user=request.user, voting=choosedVoting)
        vote.save()
        return HttpResponseRedirect('/voting/%i'%int(request.GET.get('btnFor')))
    elif(request.GET.get('btnAgainst')):
        tId = int(request.GET.get('btnAgainst'))
        choosedVoting = Voting.objects.filter(id=tId)[0]
        if len(VoteAgainst.objects.filter(user=request.user, voting=choosedVoting)) or len(VoteFor.objects.filter(user=request.user, voting=choosedVoting)):
            return HttpResponseRedirect('/voting/%i'%int(request.GET.get('btnAgainst'))) 
        vote = VoteAgainst(user=request.user, voting=choosedVoting)
        vote.save()
        return HttpResponseRedirect('/voting/%i'%int(request.GET.get('btnAgainst')))
    return render(request, 'index.html')

def deleteVoting(request):
    if request.GET.get('btnDel'):
        tId = int(request.GET.get('btnDel'))
        choosedVoting = Voting.objects.filter(id=tId)
        if len(choosedVoting) == 0:
            return HttpResponseRedirect('/del')
        choosedVoting.delete()
        return HttpResponseRedirect('/del')
    return render(request, 'index.html')

def voting(request, voting_id):
    voting = Voting.objects.filter(id=voting_id)

    if len(voting) == 0:
        raise Http404
    
    votesFor = list(VoteFor.objects.filter(voting=voting_id))
    votesAgainst = list(VoteAgainst.objects.filter(voting=voting_id))
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
        userVoteFor = VoteFor.objects.filter(voting=voting_id, user=request.user)
        userVoteAgainst = VoteAgainst.objects.filter(voting=voting_id, user=request.user)
    
    isVoted = False

    if len(userVoteFor) != 0 or len(userVoteAgainst) != 0:
        isVoted = True
    
    context={
        'voting':voting[0],
        'votesFor':len(votesFor),
        'votesAgainst': len(votesAgainst),
        'percent': percent,
        'isVoted': isVoted
    }

    return render(request, 'voting.html', context=context)

class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        votings = list(Voting.objects.all())
        votings.sort(key=lambda x: x.date, reverse=True)
        self.extra_context = {
            'votings': votings
        }
        return super().get_context_data(**kwargs)
        
    def get_success_url(self):
        return reverse_lazy('index')

class CreateVoting(LoginRequiredMixin, CreateView):
    form_class = CreateVotingForm
    template_name = 'form.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Создать голосование'
        context["button_text"] = "Создать"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect('index')

class PersonalArea(LoginRequiredMixin, TemplateView):
    template_name='personal.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        user_votings = list(Voting.objects.filter(user=self.request.user))
        user_votings.sort(key=lambda x: x.date, reverse=True)
        self.extra_context = {
            'uservotings': user_votings,
            'lenVotings': len(user_votings)
        }
        return super().get_context_data(**kwargs)

class DeleteVotings(StaffRequiredMixin, TemplateView):
    template_name = 'deleteVotings.html'
    login_url = 'login'
    def get_context_data(self, *, object_list=None, **kwargs):
        votings = list(Voting.objects.exclude(user=self.request.user))
        votings.sort(key=lambda x: x.date, reverse=True)
        self.extra_context = {
            'votings': votings
        }
        return super().get_context_data(**kwargs)