from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    """ User Registration Form """

    email = forms.EmailField()

    class Meta:
        """ Metadata """

        # save it to the model
        # Whenever this forms validates, this is going to create a new User
        model = User

        # fields are going to be shown on our form and in what order
        fields = ['username', 'email', 'password1', 'password2']
