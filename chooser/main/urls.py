from django.urls import path

from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('voting/<int:voting_id>', voting, name='voting'),
    path('create/', CreateVoting.as_view(), name='create'),
    path('personal/', PersonalArea.as_view(), name='personal'),
    path('voting/getVote', getVote, name='vote'),
    path('del/', DeleteVotings.as_view(), name='deleteVotings'),
    path('del/deleteVoting', deleteVoting, name='delete'),
    path('personal/getStaffRequest', getStaffRequest, name='getstaffRequest'),
    path('requests/', StaffRequests.as_view(), name='staffRequests'),
    path('requests/getStaffRequestSubmit', getStaffRequestSubmit, name='getStaffRequestSubmit'),
    path('staff', StaffPage.as_view(), name='staff')
]