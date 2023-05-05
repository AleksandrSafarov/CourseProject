from django.contrib import admin
from .models import *

admin.site.register(Theme)
admin.site.register(VoteAgainst)
admin.site.register(VoteFor)