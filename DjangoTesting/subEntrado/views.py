from datetime import time
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Appointment
from .forms import AppointmentForm
from.models import Staff
#login imports
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
#decorator imports
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group
#valiation for time imports
from .validators import validate_within_time_range
# email functionality
from django.core.mail import send_mail

# Create your views here.
@unauthenticated_user
def index(request):
    return render(request, 'index.html' )


#------------------------------------------------------------------------------------------------------------
                                                #LOGIN SYSTEM VIEWS
@unauthenticated_user
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            #auto assigns a user in the student group
            group = Group.objects.get(name='student')
            user.groups.add(group)

            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()
    
    return render(request,'registration/sign_up.html', {"form":form})


@login_required(login_url='/login')
def home(request):
    return render(request,"home.html")
#..........................................................................................................

                                            #Admin/Student CRUD related views

# this function displays all the appointment made
@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin'])
def appointment_list(request):
     context = {"appointment_list":Appointment.objects.all()}
     return render(request, "appointment_list.html", context)


#Deals with inserting and updating appointments
@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin', 'student'])
def appointment_form(request, id=0):
     if request.method == "GET":
        if id == 0:#<- if it is a insert
            form = AppointmentForm()
        else:#<- if it is an update
            appointment = Appointment.objects.get(pk=id)
            form = AppointmentForm(instance=appointment)
        return render(request,"appointment_form.html", {'form':form})
     else:
        if id ==0:
            form = AppointmentForm(request.POST)
        else:
            appointment = Appointment.objects.get(pk=id)
            form = AppointmentForm(request.POST,instance=appointment)

        # checks if the correct time is entered before savin in database
        if form.is_valid():
            hours = form.cleaned_data.get('time')
            if not validate_within_time_range(hours):
                form.add_error('time', 'Please choose a time within working hours (10:00 AM - 3:00 PM).')
                return render(request, "appointment_form.html", {'form': form})
            else:
                form.save()      
                
                   #appointment confirmation email, add if statements to differentiate inserts and updates, then add deletes below
            
                mailTo = request.user.email
                emailString = str ("Your request for an appointment has been logged.")
                if id ==0: #<- it is a insert
                    send_mail(
                    'Appointment Created', #subject line
                    emailString, #message line
                    'advisorybuddy03@gmail.com', #our emailing address/ variable to be used goes here
                    [mailTo,]   ) #receiver(s) email
                else:
                    emailString = str ("Your appointment for the purpose of '"+ appointment.description + "' has been updated.")
                    send_mail(
                    'Appointment Updated', #subject line
                    emailString, #message line
                    'advisorybuddy03@gmail.com', #our emailing address/ variable to be used goes here
                    [mailTo,]   ) #receiver(s) email

     # checks to see if the user is a student or admin to redirect them to the correct page after submission
                if request.user.is_authenticated:
                    for group in request.user.groups.all():
                        if group.name == "admin":
                            return redirect('appointment_list')
                        else:
                            return redirect('stu_appointment_list')
                return redirect('login')  # Handle the case where the user is not authenticated
            
        return render(request, "appointment_form.html", {'form': form})
   
#Deals with deleting appoinments
@login_required(login_url='/login')
@allowed_users(allowed_roles=['admin', 'student','staff'])
def appointment_delete(request, id):
    appointment = Appointment.objects.get(pk=id)

     #sends email to student about deleted appointment
     
    mailTo = appointment.email
    emailString = str ("Your appointment for the purpose of '"+ appointment.description + "' has been deleted.") 
    send_mail(
                    'Appointment Deleted', #subject line
                    emailString, #message line
                    'advisorybuddy03@gmail.com', #our emailing address/ variable to be used goes here
                    [mailTo,]   ) #receiver(s) email
    
    appointment.delete()

    if request.user.is_authenticated:
        for group in request.user.groups.all():
            if group.name == "student":
                return redirect('stu_appointment_list')
            if group.name == "staff":
                return redirect('staff_appointment_list')
  
        # If the user is not in the 'student' or 'staff' group, assume they are 'admin'
        return redirect('appointment_list')
    return redirect('login')

#...........................................................................................................

                                        #STUDENT APPOINTMENT VIEWS
                                        
# displays all appointments assoicated to a student
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'student'])
def stu_appointment_list(request):
    email = request.user.email  
    appointments = Appointment.objects.filter(email=email)
    context = {"appointment_list": appointments}
    return render(request, "stu_appointment_list.html", context)

#................................................................................................................
                                        #STAFF APPOINTMENT VIEWS 

# ENTER THE VIEW FOR THE STAFF TO SEE THIER APPOINTMENTS HERE

# displays all appointments assoicated to a staff member
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'staff'])
def staff_appointment_list(request):

    # concatentates the first and last name of the user to search through the staff table
    name = request.user.first_name +" "+ request.user.last_name 
    

   
     # Perform a case-insensitive search for the user's full name in the staff table
    staff_member = Staff.objects.get(fullname__iexact=name)

     # Retrieve the department_id from the matching staff member
    id = staff_member.department_id


        
    appointments = Appointment.objects.filter(person_of_intrest=id)
    context = {"appointment_list": appointments}
    return render(request, "staff_appointment_list.html", context)

#................................................................................................................
                                        #GENERAL VIEWS
@login_required(login_url='/login')
def courses(request):
    return render(request, 'courses.html')

@login_required(login_url='/login')
def info(request):
    return render(request, 'info.html')





