from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .forms import RegisterForm, ProfileUpdateForm
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .models import Profile


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile.html'

    def get_object(self):
        username = self.kwargs.get('username')
        if username:
            user = get_object_or_404(User, username=username)
            return user.profile
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.get_object().user == self.request.user
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile
