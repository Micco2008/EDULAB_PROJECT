from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
    UserChangeForm, UserCreationForm,
)
from django.contrib.auth.models import User
from django.forms import ModelForm

__all__ = ['UserCreationForm', 'ModelForm', 'User']


class TailwindForms:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = '"shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"'


class CustomLoginForm(TailwindForms, AuthenticationForm):
    pass


class CustomPasswordResetForm(TailwindForms, PasswordResetForm):
    pass


class CustomPasswordChangeForm(TailwindForms, PasswordChangeForm):
    pass


class CustomPasswordResetConfirmForm(TailwindForms, SetPasswordForm):
    pass


class CustomUserChangeForm(TailwindForms, UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)

    class Meta(UserChangeForm.Meta):
        model = User
        exclude = ['password']
        fields = ['first_name', 'email']
        labels = {'first_name': 'Имя', 'email': 'Почта'}


class CustomUserCreationForm(TailwindForms, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user
