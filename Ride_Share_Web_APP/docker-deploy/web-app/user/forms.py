from django import forms
from user.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import User
from datetime import datetime, timedelta, tzinfo
from .models import Profile, Vehicle, Order, DriverToVehicle

class vehicheForm(forms.ModelForm):
    plate_num = forms.CharField()
    vehicle_type = forms.CharField()
    max_capacity = forms.IntegerField()
    special_info = forms.CharField()
    class Meta:
        model = Vehicle
        fields = ['plate_num', 'vehicle_type', 'max_capacity', 'special_info']

class profileForm(forms.ModelForm):
    is_driver = forms.BooleanField()
    class Meta:
        model = Profile
        fields = ['is_driver']


class userForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class UserProfileUpdateForm(forms.Form):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username',  'email']


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class requestRideForm(forms.ModelForm):
    arrival_time = forms.DateTimeField()
    destination = forms.CharField()
    capacity = forms.IntegerField()
    vehicle_type = forms.CharField()
    is_shared = forms.CharField()
    special_info = forms.CharField()

    class Meta:
        model = Order
        fields = ['arrival_time','destination', 'capacity', 'vehicle_type', 'is_shared', 'special_info']

'''//////////////////////'''   
class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class orderSearchForm(forms.Form):
    destination = forms.CharField(label = 'Destination')
    number = forms.IntegerField(label = 'Number of passengers')
    start = forms.DateTimeField(label = 'Earlist Time',
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'})
        )
    end = forms.DateTimeField(label = 'Latest Time',
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'})
        )

class driverSearchForm(forms.Form):
    vechicle_type = forms.CharField(label = 'Type of vechicle')
    number = forms.IntegerField(label = 'Number of passengers')
    start = forms.DateTimeField(label = 'Earlist Time',
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'})
        )

    end = forms.DateTimeField(label = 'Latest Time',
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'})
        )
 