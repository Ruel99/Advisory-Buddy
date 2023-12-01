from django.db import models
from .validators import validate_within_time_range

# Create your models here.
class Department(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

   
class Staff(models.Model):
    fullname = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.fullname 

class Appointment(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    person_of_intrest = models.ForeignKey(Staff, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True, validators=[validate_within_time_range])
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
