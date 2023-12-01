from django import forms
from .models import Appointment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime, time
from .validators import validate_within_time_range

#Stuff for the login system
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model= User
        fields = ["username", "first_name", "last_name","email", "password1", "password2"]


#this class is used to make a form with fields of the attributes in the appointment table
class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'DD-MM-YYYY'}),
        input_formats=['%Y-%m-%d']  # Specify the desired date format
    )

    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}),validators=[validate_within_time_range])

    class Meta:
        model = Appointment
        fields = ('fullname', 'email', 'mobile', 'person_of_intrest', 'department', 'description', 'date', 'time')
        labels = {
            'fullname': 'Full Name',
        }

    #to style the dropdown menu in the department field
    def __init__(self, *args, **kwargs):
        super(AppointmentForm,self).__init__(*args, **kwargs)
        self.fields['department'].empty_label = "Select Department"
        self.fields['person_of_intrest'].empty_label = "Choose a Staff Member"
        self.fields['date'].required = True
        

"""
def clean_time(self):
        hours = self.cleaned_data.get('time')
        validate_within_time_range(hours)
        return hours
"""    

      
 