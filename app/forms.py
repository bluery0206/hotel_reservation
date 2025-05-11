from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator, MinLengthValidator, FileExtensionValidator

from .models import Profile, Amenity, Room

class SignUpForm(UserCreationForm):
    """ User Registration Form """

    email = forms.EmailField(
        widget = forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "example@domain.com",
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
                'placeholder': "example_example02",
        })
    )
    first_name = forms.CharField(
        validators = [
            RegexValidator(
                r'^[a-zA-Z\s]+$',
                message = "Letters only."
            )
        ],
        widget = forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "Juan",
        })
    )
    last_name = forms.CharField(
        validators = [
            RegexValidator(
                r'^[a-zA-Z\s]+$',
                message = "Letters only."
            )
        ],
        widget = forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "Dela Cruz",
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
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    """ Profile update Form """

    image = forms.FileField(
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'jfif', 'PNG', 'JPG'])],
        allow_empty_file = True,
        required = False,
        widget = forms.FileInput(attrs={
            'class' : 'form-control',
        }),
    )

    class Meta:
        """ Metadata """

        # save it to the model
        # Whenever this forms validates, this is going to create a new User
        model = Profile

        # fields are going to be shown on our form and in what order
        fields = ['image']


class UserUpdateForm(forms.ModelForm):
    """ Profile update Form """

    email = forms.EmailField(
        widget = forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "example@domain.com",
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
                'placeholder': "example_example02",
        })
    )
    first_name = forms.CharField(
        validators = [
            RegexValidator(
                r'^[a-zA-Z\s]+$',
                message = "Letters only."
            )
        ],
        widget = forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "Juan",
        })
    )
    last_name = forms.CharField(
        validators = [
            RegexValidator(
                r'^[a-zA-Z\s]+$',
                message = "Letters only."
            )
        ],
        widget = forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder': "Dela Cruz",
        })
    )

    class Meta:
        """ Metadata """

        # save it to the model
        # Whenever this forms validates, this is going to create a new User
        model = User

        # fields are going to be shown on our form and in what order
        fields = ['first_name', 'last_name', 'username', 'email']


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
        widget = forms.PasswordInput(attrs={
            'class' : 'form-control',
            'placeholder': "Your password",
        })
    )

    class Meta:
        """ Metadata """

        model 	= User
        fields 	= ['username', 'password']


class AmenityForm(forms.ModelForm):
    """ Form for adding amenity"""

    name = forms.CharField(
        validators = [
            RegexValidator(
                r'^[a-zA-Z0-9_.\s-]{2,}$',
                message = 'Allowed characters: a-z, A-Z, 0-9, "_", ".", "-"'
            )
        ],
        widget = forms.TextInput(attrs={
            'class' : 'form-control',
            'placeholder': "TV",
        })
    )

    class Meta:
        model = Amenity
        fields = ['name']


class RoomForm(forms.ModelForm):
    class Meta:
        # save it to the model
        # Whenever this forms validates, this is going to create a new User
        model = Room

        # fields are going to be shown on our form and in what order
        fields = [
            'image', 
            'name', 
            'description', 
            'type', 
            'amenities', 
            'base_price', 
            'capacity', 
        ]
        widgets = {
            'image': forms.FileInput(attrs={
                    'class' : 'form-control',
                }
            ),
            'name': forms.TextInput(attrs={
                    'class' : 'form-control',
                    'placeholder': "E.g.: Classic Standard",
                }
            ),
            "description": forms.Textarea(attrs={
                    'rows': 2,
                    'class': 'form-control',
                    'placeholder': "E.g.: Lorem ipsum",
                }
            ),
            "type": forms.Select(attrs={
                    'class' : 'form-select',
                }
            ),
            "amenities": forms.CheckboxSelectMultiple(attrs={
                    'class' : 'form-check-input',
                    'required' : False,
                }
            ),
            "base_price": forms.NumberInput(attrs={
                    'class' : 'form-control',
                    'min': 0,
                }
            ),
            "capacity": forms.NumberInput(attrs={
                    'class' : 'form-control',
                    'min': 0,
                    'step': 1,
                }
            )
        }

