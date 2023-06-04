from django.contrib import admin
from .models import *

admin.site.register(Voting)
admin.site.register(VoteAgainst)
admin.site.register(VoteFor)
admin.site.register(StaffRequest)
admin.site.register(Complaint)