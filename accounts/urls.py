from django.urls import path
from .views import RegisterView, ProfileDetailView, ProfileUpdateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('profile/', ProfileDetailView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='user_profile'),
]