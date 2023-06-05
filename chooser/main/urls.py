from django.urls import path

from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('create/', CreateVoting.as_view(), name='create'),
    path('personal/', PersonalArea.as_view(), name='personal'),
    path('del/', DeleteVotings.as_view(), name='deleteVotings'),
    path('requests/', StaffRequests.as_view(), name='staffRequests'),
    path('staff/', StaffPage.as_view(), name='staff'),
    path('complaints/', ComplaintPage.as_view(), name='complaints'),
    path('voting/<int:voting_id>', voting, name='voting'),
    path('voting/getVote', getVote, name='vote'),
    path('del/deleteVoting', deleteVoting, name='delete'),
    path('personal/getStaffRequest', getStaffRequest, name='getstaffRequest'),
    path('requests/getStaffRequestSubmit', getStaffRequestSubmit, name='getStaffRequestSubmit'),
    path('complaints/complaintSubmit', complaintSubmit, name='complaintSubmit'),
    path('voting/createComplaint', createComplaint, name='createComplaint')
]