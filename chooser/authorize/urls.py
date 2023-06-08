from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('logout/', logout_user, name='logout'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('edituserdata/', ChangeUserData.as_view(), name='edituserdata'),
    path('changepassword/', ChangePassword.as_view(), name='changepassword')
]