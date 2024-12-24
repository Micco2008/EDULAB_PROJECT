from django.contrib.auth import views as auth_views
from django.urls import path

from users import forms, views
from users.views import (
    CustomLoginView, CustomPasswordChangeView, CustomPasswordResetConfirmView,
    CustomPasswordResetView,
)

__all__ = ['views', 'forms', 'path']

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
]

auth_patterns = [
    path(
        'login/',
        CustomLoginView.as_view(),
        name='login',
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(template_name='users/logout.html'),
        name='logout',
    ),
    path(
        'password_change/',
        CustomPasswordChangeView.as_view(
            template_name='users/password_change.html',
        ),
        name='password_change',
    ),
    path(
        'password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html',
        ),
        name='password_change_done',
    ),
    path(
        'password_reset/',
        CustomPasswordResetView.as_view(),
        name='password_reset',
    ),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        CustomPasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
]

urlpatterns += auth_patterns

