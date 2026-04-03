from django.views.generic import ListView, CreateView, UpdateView, DeleteView, RedirectView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import Achievement, UserAchievement
from .forms import AchievementForm

class AchievementListView(ListView):
    model = Achievement
    template_name = 'achievements/all_achievements.html'

class UserAchievementView(LoginRequiredMixin, ListView):
    model = UserAchievement
    template_name = 'achievements/my_achievements.html'

    def get_queryset(self):
        self.profile_user = get_object_or_404(User, username=self.kwargs['username'])
        return UserAchievement.objects.filter(user=self.profile_user).select_related('achievement')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = self.profile_user
        return context


class MyAchievementsRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('my_achievements', kwargs={'username': self.request.user.username})

class AchievementCreateView(LoginRequiredMixin, CreateView):
    model = Achievement
    form_class = AchievementForm
    template_name = 'achievements/achievement_form.html'
    success_url = reverse_lazy('all_achievements')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class CreatorOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().creator_id == self.request.user.id

    def handle_no_permission(self):
        raise PermissionDenied("Only the creator can edit or delete this achievement.")


class AchievementUpdateView(LoginRequiredMixin, CreatorOnlyMixin, UpdateView):
    model = Achievement
    form_class = AchievementForm
    template_name = 'achievements/achievement_form.html'
    success_url = reverse_lazy('all_achievements')


class AchievementDeleteView(LoginRequiredMixin, CreatorOnlyMixin, DeleteView):
    model = Achievement
    template_name = 'achievements/achievement_confirm_delete.html'
    success_url = reverse_lazy('all_achievements')
