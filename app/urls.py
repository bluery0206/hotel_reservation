from django.urls import path
from django.contrib.auth.views import (
	PasswordResetView,
	PasswordResetDoneView,
    PasswordResetConfirmView,
	PasswordResetCompleteView,
)

from . import views

urlpatterns = [
	path("", views.index, name="app-index"),
	path("signin/", views.signin, name="app-signin"),
	path("signup/", views.signup, name="app-signup"),
	path("signout/", views.signout, name="app-signout"),

	path("signin/forgot_password/reset/", PasswordResetView.as_view(
		template_name='app/auth/password_reset/password_reset.html'
        ),name="password-reset"),
	path("signin/forgot_password/reset/confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(
        template_name='app/auth/password_reset/password_reset_confirm.html'),
        name="password_reset_confirm"),
	path("signin/forgot_password/reset/done/", PasswordResetDoneView.as_view(
        template_name='app/auth/password_reset/password_reset_done.html'),
        name="password_reset_done"),
	path("signin/forgot_password/reset/complete/", PasswordResetCompleteView.as_view(
        template_name='app/auth/password_reset/password_reset_complete.html'),
        name="password_reset_complete"),
]
