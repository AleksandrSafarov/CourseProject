from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import *
import datetime

from .models import *
from .forms import *
from .utils import StaffRequiredMixin

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import numpy as np


def getStaffRequestSubmit(request):
    if request.GET.get('btnAccept'):
        uId = int(request.GET.get('btnAccept'))
        choosedUser = User.objects.filter(id=uId)[0]
        choosedRequest = StaffRequest.objects.filter(user=choosedUser)[0]
        if choosedRequest.status == 0:
            StaffRequest.objects.filter(user=choosedUser).update(status=1)
            User.objects.filter(id=uId).update(is_staff=True)
        return HttpResponseRedirect('/requests')
    if request.GET.get('btnDecline'):
        uId = int(request.GET.get('btnDecline'))
        choosedUser = User.objects.filter(id=uId)[0]
        choosedRequest = StaffRequest.objects.filter(user=choosedUser)[0]
        if choosedRequest.status == 0:
            StaffRequest.objects.filter(user=choosedUser).update(status=2)
        return HttpResponseRedirect('/requests')
        

def getStaffRequest(request):
    if request.GET.get('btnRequest') and request.user.is_authenticated:
        requests = StaffRequest.objects.filter(user=request.user)
        if len(requests) == 0:
            r = StaffRequest(user=request.user)
            r.save()
    return HttpResponseRedirect('/personal')

def getVote(request):
    if(request.GET.get('btnFor')):
        vId = int(request.GET.get('btnFor'))
        choosedVoting = Voting.objects.filter(id=vId)[0]
        if len(VoteFor.objects.filter(user=request.user, voting=choosedVoting)) or len(VoteAgainst.objects.filter(user=request.user, voting=choosedVoting)):
            return HttpResponseRedirect('/voting/%i'%int(request.GET.get('btnFor'))) 
        vote = VoteFor(user=request.user, voting=choosedVoting)
        vote.save()
        return HttpResponseRedirect('/voting/%i'%int(request.GET.get('btnFor')))
    elif(request.GET.get('btnAgainst')):
        vId = int(request.GET.get('btnAgainst'))
        choosedVoting = Voting.objects.filter(id=vId)[0]
        if len(VoteAgainst.objects.filter(user=request.user, voting=choosedVoting)) or len(VoteFor.objects.filter(user=request.user, voting=choosedVoting)):
            return HttpResponseRedirect('/voting/%i'%int(request.GET.get('btnAgainst'))) 
        vote = VoteAgainst(user=request.user, voting=choosedVoting)
        vote.save()
        return HttpResponseRedirect('/voting/%i'%int(request.GET.get('btnAgainst')))
    return HttpResponse('')

def deleteVoting(request):
    if request.GET.get('btnDelete'):
        vId = int(request.GET.get('btnDelete'))
        choosedVoting = Voting.objects.filter(id=vId)
        choosedVoting.delete()
        return HttpResponseRedirect('/delete')
    return HttpResponse('')

def deleteUserVoting(request):
    if request.GET.get('btnDelete'):
        vId = int(request.GET.get('btnDelete'))
        choosedVoting = Voting.objects.filter(id=vId)
        choosedVoting.delete()
        return HttpResponseRedirect('/personal/')
    return HttpResponse('')

def complaintSubmit(request):
    if request.GET.get('btnDelete'):
        cId = int(request.GET.get('btnDelete'))
        choosedComplaint = Complaint.objects.get(id=cId)
        choosedVoting = choosedComplaint.voting
        choosedVoting.delete()
    if request.GET.get('btnDecline'):
        cId = int(request.GET.get('btnDecline'))
        choosedComplaint = Complaint.objects.get(id=cId)
        choosedComplaint.delete()
    return HttpResponseRedirect('/complaints')

def createComplaint(request):
    if request.GET.get('btnCreate'):
        vId = int(request.GET.get('btnCreate'))
        complaint = Complaint(voting=Voting.objects.filter(id=vId)[0], user=request.user)
        complaint.save()
    return HttpResponseRedirect('/voting/%i'%int(request.GET.get('btnCreate'))) 

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
    
    userComplaint=[]

    if request.user.is_authenticated:
        userComplaint = Complaint.objects.filter(user=request.user, voting=voting_id)

    if len(votesFor)!=0 and len(votesAgainst)!=0:
        labels = 'За', 'Против'
        sizes = [len(votesFor),len(votesAgainst)]
        explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90, colors=((0, 1, 0, 1),(1, 0, 0, 1)))
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.savefig('static/images/chart.png',dpi=200)

    context={
        'voting':voting[0],
        'votesFor':len(votesFor),
        'votesAgainst': len(votesAgainst),
        'percent': percent,
        'isVoted': isVoted,
        'isComplaintCreated': len(userComplaint)!=0,
        'sumVotes': len(votesFor)+len(votesAgainst)
    }

    return render(request, 'voting.html', context=context)

class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        votings = list(Voting.objects.all())
        if self.request.user.is_authenticated:
            votings = list(Voting.objects.all().exclude(user=self.request.user))
        votings.sort(key=lambda x: x.date, reverse=True)
        votingsAndVotes=[]
        for v in votings:
            votesFor = len(list(VoteFor.objects.filter(voting=v)))
            votesAgainst = len(list(VoteAgainst.objects.filter(voting=v)))
            votingsAndVotes.append([v, votesFor+votesAgainst])
        self.extra_context = {
            'votings': votingsAndVotes
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
        form.instance.date = datetime.datetime.now()
        form.save()
        return redirect('index')

class PersonalArea(LoginRequiredMixin, TemplateView):
    template_name='personal.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        userVotings = list(Voting.objects.filter(user=self.request.user))
        userVotings.sort(key=lambda x: x.date, reverse=True)
        userVotingAndVotes=[]
        for v in userVotings:
            votesFor = len(list(VoteFor.objects.filter(voting=v)))
            votesAgainst = len(list(VoteAgainst.objects.filter(voting=v)))
            userVotingAndVotes.append([v, votesFor+votesAgainst])
        staffR = StaffRequest.objects.filter(user=self.request.user)
        isRequestCreated = False
        if len(staffR)==0:
            requestStatus = 0
        else:
            isRequestCreated = True
            requestStatus = staffR[0].status
        self.extra_context = {
            'uservotings': userVotingAndVotes,
            'lenVotings': len(userVotings),
            'isRequestCreated': isRequestCreated,
            'status': requestStatus
        }
        return super().get_context_data(**kwargs)

class DeleteVotings(StaffRequiredMixin, TemplateView):
    template_name = 'deleteVotings.html'
    login_url = 'login'
    def get_context_data(self, *, object_list=None, **kwargs):
        votings = list(Voting.objects.all())
        votings.sort(key=lambda x: x.date, reverse=True)
        votingsAndVotes = []
        for v in votings:
            votesFor = len(list(VoteFor.objects.filter(voting=v)))
            votesAgainst = len(list(VoteAgainst.objects.filter(voting=v)))
            votingsAndVotes.append([v, votesFor+votesAgainst])
        self.extra_context = {
            'votings': votingsAndVotes
        }
        return super().get_context_data(**kwargs)

class StaffRequests(StaffRequiredMixin, TemplateView):
    template_name = 'staffRequests.html'
    login_url = 'login'
    def get_context_data(self, *, object_list=None, **kwargs):
        staffRequests = StaffRequest.objects.filter(status=0)
        userInfo = []
        for s in staffRequests:
            userVotings = len(list(Voting.objects.filter(user=s.user)))
            votes = len(list(VoteFor.objects.filter(user=s.user))) + len(list(VoteAgainst.objects.filter(user=s.user)))
            userInfo.append([s, userVotings, votes])
        self.extra_context = {
            'staffRequests': userInfo
        }
        return super().get_context_data(**kwargs)

class StaffPage(StaffRequiredMixin, TemplateView):
    template_name = 'staffPage.html'
    login_url = 'login'
    def get_context_data(self, *, object_list=None, **kwargs):
        self.extra_context = {}
        return super().get_context_data(**kwargs)

class ComplaintPage(StaffRequiredMixin, TemplateView):
    template_name = 'complaints.html'
    login_url = 'login'
    def get_context_data(self, *, object_list=None, **kwargs):
        complaints = Complaint.objects.all().exclude(user=self.request.user)
        for complaint in complaints:
            print(complaint.voting.title)
        self.extra_context = {
            'complaints': complaints
        }
        return super().get_context_data(**kwargs)