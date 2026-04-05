from django.views.generic import ListView
from .forms import ChallengeForm
from .mixins import OwnerRequiredMixin
from .models import Challenge
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import UpdateView
from django.views.generic import DeleteView


class ChallengeListView(ListView):
    model = Challenge
    template_name = 'challenges/challenge_list.html'
    context_object_name = 'challenges'

    def get_queryset(self):
        queryset = super().get_queryset()
        difficulty = self.request.GET.get('difficulty')

        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        return queryset

class ChallengeDetailView(DetailView):
    model = Challenge
    template_name = 'challenges/challenge_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_contestant'] = self.object.contestants.filter(id=self.request.user.id).exists()
        return context

class ChallengeCreateView(LoginRequiredMixin, CreateView):
    model = Challenge
    form_class = ChallengeForm
    template_name = 'challenges/challenge_create.html'
    success_url = reverse_lazy('challenge_list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f"Challenge '{self.object.title}' was created successfully.")
        return response

class ChallengeUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Challenge
    form_class = ChallengeForm
    template_name = 'challenges/challenge_edit.html'
    success_url = reverse_lazy('challenge_list')

class ChallengeDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Challenge
    template_name = 'challenges/challenge_delete.html'
    success_url = reverse_lazy('challenge_list')
