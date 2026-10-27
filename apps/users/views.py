from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm, ProfileForm


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'registration/profile.html'
    success_url = 'registration/register.html'

    def get_object(self):
        return self.request.user
