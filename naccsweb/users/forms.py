from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class PlayerSearchForm(forms.Form):
    query = forms.CharField(label="Player Name", min_length=3,
                            widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    
class CustomAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        return self.cleaned_data.get('username').lower()

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_username(self):
        return self.cleaned_data.get('username').lower()

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('An account with that e-mail already exists')

        password = cleaned_data.get('password')
        validate_password(password)

        confirm = cleaned_data.get('confirm')
        if confirm != password:
            raise ValidationError("Passwords do not match")

        return cleaned_data

    username = forms.CharField(label="Username", max_length=32)
    email    = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)
    confirm  = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)