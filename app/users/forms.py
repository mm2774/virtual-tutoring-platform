from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class CreateUserForm(UserCreationForm):
    username = forms.CharField(label=(u'User Name'))
    email = forms.EmailField(label = (u'Email Address'))
    first_name = forms.CharField(label=(u'First Name'))
    last_name = forms.CharField(label=(u'Last Name'))

    def clean_email(self):
        data = self.cleaned_data['email']
        if "@cornell.edu" not in data:   # any check you need
            raise forms.ValidationError("Must be a Cornell email address")
        return data

    class Meta:
        model = User
        fields = ['username','email', 'first_name', 'last_name', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['grad_year','college','image']

