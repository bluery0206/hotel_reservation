from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator, MinLengthValidator, FileExtensionValidator

from . import models



class SignUpForm(UserCreationForm):
    # Custom validators because django doesnt have validation for names
    first_name = forms.CharField(
        validators=[RegexValidator(
                r'^[a-zA-Z\s]+$', 
                message="Letters only."
        )],
        widget = forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder': "Juan",
        }),
    )
    last_name = forms.CharField(
        validators=[RegexValidator(
            r'^[a-zA-Z\s]+$', 
            message="Letters only."
        )],
        widget = forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder': "Dela Cruz",
        }),
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
        # save it to the model
        # Whenever this forms validates, this is going to create a new User
        model = User

        # fields are going to be shown on our form and in what order
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets = {
            "email": forms.EmailInput(attrs={
                'class' : 'form-control',
                'placeholder': "example@domain.com",
                'minlength': 4,
            }),
            "username": forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "example_example02",
            }),
        }



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['image']
        widgets = {
            "image": forms.FileInput(attrs={
                'class' : 'form-control',
            }),
        }



class UserUpdateForm(forms.ModelForm):
    # Custom validators because django doesnt have validation for names
    first_name=forms.CharField(
        validators=[
            RegexValidator(r'^[a-zA-Z\s]+$', 
            message="Letters only.")
        ],
        widget=forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder': "Juan",
        }),
    )
    last_name = forms.CharField(
        validators=[
            RegexValidator(r'^[a-zA-Z\s]+$', 
            message="Letters only.")
        ],
        widget=forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder': "Dela Cruz",
        }),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            "email": forms.EmailInput(attrs={
                'class' : 'form-control',
                'placeholder': "example@domain.com",
                'minlength': 4,
            }),
            "username": forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "example_example02",
            }),
        }



class SignInForm(AuthenticationForm):
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
        widget = forms.PasswordInput(attrs={
            'class' : 'form-control',
            'placeholder': "Your password",
        })
    )

    class Meta:
        model 	= User
        fields 	= ['username', 'password']



class AmenityForm(forms.ModelForm):
    class Meta:
        model = models.Amenity
        fields = ['name', 'fee']
        widgets = {
            'name': forms.TextInput(attrs={
                    'class' : 'form-control',
                    'placeholder': "E.g.: Classic Standard",
            }),
            "fee": forms.NumberInput(attrs={
                    'class' : 'form-control',
                    'min': 0,
            }),
        }



class RoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = ['image', 'name', 'description', 'type', 'amenities', 'base_price', 'capacity']
        widgets = {
            'image': forms.FileInput(attrs={
                    'class' : 'form-control',
            }),
            'name': forms.TextInput(attrs={
                    'class' : 'form-control',
                    'placeholder': "E.g.: Classic Standard",
            }),
            "description": forms.Textarea(attrs={
                    'rows': 2,
                    'class': 'form-control',
                    'placeholder': "E.g.: Lorem ipsum",
            }),
            "type": forms.Select(attrs={
                    'class' : 'form-select',
            }),
            "amenities": forms.CheckboxSelectMultiple(attrs={
                    'class' : 'form-check-input',
                    'required' : False,
            }),
            "base_price": forms.NumberInput(attrs={
                    'class' : 'form-control',
                    'min': 0,
            }),
            "capacity": forms.NumberInput(attrs={
                    'class' : 'form-control',
                    'min': 0,
                    'step': 1,
            })
        }




class ReservationForm(forms.ModelForm):
    class Meta:
        model = models.Reservation
        fields = [
            'date_bookfrom',
            'date_bookuntil',
        ]
        widgets = {
            'date_bookfrom': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class' : 'form-control',
                    'type': 'date',
                },
            ),
            'date_bookuntil': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class' : 'form-control',
                    'type': 'date',
                },
            ),
        }
