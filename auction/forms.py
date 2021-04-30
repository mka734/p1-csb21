from django import forms
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone


# Vulnerability (validation should be stricter)
class AddItemForm(forms.Form):
    name = forms.CharField(label='Name', min_length=1, max_length=50)
    starting_price = forms.IntegerField(
        label='Starting Price', min_value=1, max_value=100000)
    min_increment = forms.IntegerField(
        label='Minimum Price Increment', min_value=1, max_value=10000)
    location = forms.CharField(
        label='Location', min_length=1, max_length=400)
    expiration_time = forms.CharField()

    def clean(self, *args, **kwargs):
        super(AddItemForm, self).clean(*args, **kwargs)
        datetime_object = datetime.strptime(
            self.data['expiration_time'], '%a, %d %b %Y %H:%M %Z%z')
        if datetime_object < timezone.now() + timedelta(hours=1):
            print('Expiration date must be later than now.')
            raise ValidationError('Expiration date must be later than now.')


# Vulnerability (validation should be stricter)
class RegisterForm(forms.Form):
    username = forms.CharField(label='Name', min_length=2, max_length=50)
    password = forms.CharField(
        widget=forms.PasswordInput, label='Password', min_length=6, max_length=50)
    email = forms.CharField(label='Email', max_length=100)


class LoginForm(forms.Form):
    name = forms.CharField(label='Name', min_length=1, max_length=50)
    password = forms.CharField(
        widget=forms.PasswordInput, label='Password', max_length=50)
