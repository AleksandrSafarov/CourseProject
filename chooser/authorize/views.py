from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.views.generic import *

from .forms import *


class SignUp(CreateView):
    form_class = SignUpForm
    template_name = 'form.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Регистрация'
        context["button_text"] = "Зарегистрироваться"
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

class Login(LoginView):
    form_class = LoginForm
    template_name = 'form.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Вход"
        context["button_text"] = "Войти"
        return context

    def get_success_url(self):
        return reverse_lazy('index')

class ChangeUserData(LoginRequiredMixin, UpdateView):
    form_class = ChangeUserDataForm
    template_name = 'form.html'
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('login')

    def get_object(self):
        return self.request.user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактировать данные"
        context["button_text"] = "Сохранить"
        return context

class ChangePassword(LoginRequiredMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'form.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Изменить пароль"
        context["button_text"] = "Изменить"
        return context

    def form_valid(self, form):
        return super().form_valid(form)
    
def logout_user(request):
    logout(request)
    return redirect('login')