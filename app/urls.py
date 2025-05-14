from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import (
	PasswordResetView,
	PasswordResetDoneView,
    PasswordResetConfirmView,
	PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView,
)

from . import views


forgot_password_patterns = [
	path("", PasswordResetView.as_view(
			template_name='app/auth/password_reset/password_reset.html',
			extra_context={},
		),
        name="password-reset"
	),
	path("email_sent/", PasswordResetDoneView.as_view(
			template_name='app/auth/password_reset/password_reset_done.html'
		),
		name="password_reset_done"
	),
	path("validate/<uidb64>/<token>/", PasswordResetConfirmView.as_view(
			template_name='app/auth/password_reset/password_reset_confirm.html',
		),
		name="password_reset_confirm"
	),
	path("complete/", PasswordResetCompleteView.as_view(
		template_name='app/auth/password_reset/password_reset_complete.html'),
		name="password_reset_complete"),
]

password_change_patterns = [
	path("", PasswordChangeView.as_view(
			template_name='app/auth/password_change/password_change.html',
		),
		name="password-change"
	),
	path("done/", PasswordChangeDoneView.as_view(
		template_name='app/auth/password_change/password_change_done.html'),
		name="password_change_done"),
]

auth_patterns = [
	path("signin/", views.signin, name="signin"),
	path("signup/", views.signup, name="signup"),
	path("signout/", views.signout, name="signout"),
]

profile_patterns = [
	path("<uuid:pk>/", views.profile, name="index"),
]

amenity_patterns = [
	path("all/", views.amenity_index, name="index"),
	path("add/", views.add_amenity, name="add"),
	path("update/<uuid:pk>/", views.update_amenity, name="update"),
	path("delete/<uuid:pk>/", views.delete_amenity, name="delete"),
	path("delete/all", views.delete_all_amenity, name="delete_all"),
]

room_patterns = [
	path("all/", views.room_index, name="index"),
	path("add/", views.room_add, name="add"),
	path("update/<uuid:pk>/", views.room_update, name="update"),
	path("delete/<uuid:pk>/", views.room_delete, name="delete"),
	path("delete/all/", views.room_delete_all, name="delete_all"),
	path("view/<uuid:pk>/", views.room_view, name="view"),
]

urlpatterns = [
	path("", views.index, name="app-index"),

	path("auth/", include((auth_patterns, 'auth'))),
	path("auth/password_change/", include((password_change_patterns))),
	path("auth/forgot_password/", include((forgot_password_patterns))),
	path("profile/", include((profile_patterns, 'profile'))),
	path("amenity/", include((amenity_patterns, 'amenity'))),
	path("room/", include((room_patterns, 'room'))),
]
