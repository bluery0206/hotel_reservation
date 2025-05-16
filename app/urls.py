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
	path("view/<uuid:pk>/", views.profile_view, name="view"),
	path("delete/<uuid:pk>/", views.profile_delete, name="delete"),
]

amenity_patterns = [
	path("all/", views.amenity_index, name="index"),
	path("add/", views.amenity_add, name="add"),
	path("update/<uuid:pk>/", views.amenity_update, name="update"),
	path("delete/<uuid:pk>/", views.amenity_delete, name="delete"),
	path("delete/all", views.amenity_delete_all, name="delete_all"),
]


reservation_patterns = [
	path("all/", views.reservation_index, name="index"),
	path("delete/<uuid:pk>/", views.reservation_delete, name="delete"),
	path("delete/all/", views.reservation_delete_all, name="delete_all"),
	path("view/<uuid:pk>/", views.reservation_view, name="view"),
	
	path("checkin/<uuid:pk>/", views.reservation_checkin, name="checkin"),
	path("checkout/<uuid:pk>/", views.reservation_checkout, name="checkout"),
]

room_patterns = [
	path("all/", views.room_index, name="index"),
	path("add/", views.room_add, name="add"),
	path("update/<uuid:pk>/", views.room_update, name="update"),
	path("delete/<uuid:pk>/", views.room_delete, name="delete"),
	path("delete/all/", views.room_delete_all, name="delete_all"),
	path("view/<uuid:pk>/", views.room_view, name="view"),
    
	path("reservation/", include((reservation_patterns, 'reservation'))),
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
