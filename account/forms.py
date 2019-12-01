from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from account.models import User


class DateInput(forms.DateInput):
    input_type = 'date'


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Add a valid email address.')

    class Meta:
        model = User
        fields = ('email', 'username', 'date_of_birth', 'password1', 'password2',)
        widgets = {'date_of_birth' : DateInput()}


class AuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError('Invalid login')
