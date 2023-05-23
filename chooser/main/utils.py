from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):

    def test_func(self):
        if self.request.user.is_staff and self.request.user.is_authenticated:
            return True
        raise Http404