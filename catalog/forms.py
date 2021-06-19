from django import forms
from django.contrib.auth.models import User
from .models import FeedBack, Profile


class FeedBackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ['name', 'name_space', 'customer_login', 'position', 'organization', 'email', 'description']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('organization', 'position', 'photo')