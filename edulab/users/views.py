from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView,
)
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from users.forms import (
    CustomLoginForm, CustomPasswordChangeForm, CustomPasswordResetConfirmForm,
    CustomPasswordResetForm, CustomUserCreationForm,
)
from exams.models import Exam


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = CustomLoginForm


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    form_class = CustomPasswordResetForm


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change.html'
    form_class = CustomPasswordChangeForm


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    form_class = CustomPasswordResetConfirmForm


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exams'] = Exam.objects.filter(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        exam = Exam.objects.get(id=int(request.POST['exam'][0]))
        exam.delete()
        return render(request, self.template_name, self.get_context_data())

def signup(request):
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid() and request.method == 'POST':
        user = form.save(commit=False)
        user.is_active = True
        user.save()

        return redirect('login')

    return render(request, 'users/signup.html', context={'form': form})

