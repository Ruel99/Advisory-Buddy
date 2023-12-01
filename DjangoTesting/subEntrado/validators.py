from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import time

#this function checks to see the user chooses the correct time. If a time is with in the lunch hour or
#  outside the working hours a error message would be displayed in the form

def validate_within_time_range(value):
    start_time = time(10, 0) # appointments can be created from 10 AM
    end_time = time(15, 0) # last time to book an appointment 
    lunch_start = time(12, 0)
    lunch_end = time(13, 0)

    if value < start_time or value > end_time or ( value >= lunch_start and value <= lunch_end): 
        raise ValidationError(
            _('%(value)s Please note that the working hours is (10:00 AM - 3:00 PM) and the lunch hours are from 12PM - 1PM.'),
            params={'value': value},
        )

    return value

