from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator, MinLengthValidator


class SignUpForm(UserCreationForm):
    """ User Registration Form """

    email = forms.EmailField(
        widget = forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "example_example02",
                'minlength': 4,
        }),
    )
    username = forms.CharField(
        validators = [
            RegexValidator(
                r'^[a-zA-Z0-9_.]{4,}$',
                message = "Letters, numbers, underscore, and period only."
            )
        ],
        widget = forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "example@domain.com",
        })
    )
    password1 = forms.CharField(
        validators = [
            MinLengthValidator(8)
        ],
        widget = forms.PasswordInput(attrs={
                'class' : 'form-control',
                'placeholder': "Must have at least 8 characters",
        })
    )
    password2 = forms.CharField(
        validators = [
            MinLengthValidator(8)
        ],
        widget = forms.PasswordInput(attrs={
                'class' : 'form-control',
                'placeholder': "Must have at least 8 characters",
        })
    )

    class Meta:
        """ Metadata """

        # save it to the model
        # Whenever this forms validates, this is going to create a new User
        model = User

        # fields are going to be shown on our form and in what order
        fields = ['username', 'email', 'password1', 'password2']




class SignInForm(AuthenticationForm):
    """ Login Form"""

    username = forms.CharField(
        validators = [
            RegexValidator(
                r'^[a-zA-Z0-9_.]{4,}$',
                message = "Letters, numbers, underscore, and period only."
            )
        ],
        widget = forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder': "example_example02",
        })
    )
    password = forms.CharField(
        validators = [
            MinLengthValidator(8)
        ],
        widget = forms.PasswordInput(attrs={
            'class' : 'form-control',
            'placeholder': "Your password",
        })
    )

    class Meta:
        """ Metadata """

        model 	= User
        fields 	= ['username', 'password']
