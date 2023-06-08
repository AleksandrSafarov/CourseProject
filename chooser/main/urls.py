from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import *

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('create/', CreateVoting.as_view(), name='create'),
    path('personal/', PersonalArea.as_view(), name='personal'),
    path('delete/', DeleteVotings.as_view(), name='deleteVotings'),
    path('requests/', StaffRequests.as_view(), name='staffRequests'),
    path('staff/', StaffPage.as_view(), name='staff'),
    path('complaints/', ComplaintPage.as_view(), name='complaints'),
    path('voting/<int:voting_id>', voting, name='voting'),
    path('voting/getVote', getVote, name='vote'),
    path('delete/deleteVoting', deleteVoting, name='delete'),
    path('personal/getStaffRequest', getStaffRequest, name='getstaffRequest'),
    path('requests/getStaffRequestSubmit', getStaffRequestSubmit, name='getStaffRequestSubmit'),
    path('complaints/complaintSubmit', complaintSubmit, name='complaintSubmit'),
    path('voting/createComplaint', createComplaint, name='createComplaint'),
    path('personal/deleteUserVoting', deleteUserVoting, name='deleteUserVoting'),
]