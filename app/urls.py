from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name="app-index"),
	path("signin/", views.signin, name="app-signin"),
	path("signup/", views.signup, name="app-signup"),
]
