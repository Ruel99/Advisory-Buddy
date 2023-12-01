from django.urls import path, include
from django.contrib.auth import views as auth_views 
from . import views



urlpatterns =[
    
    #path ('', views.index, name ='index'),
    #path ('SE2StudentHomeV2', views.SE2StudentHomeV2, name= 'SE2StudentHomeV2'),
    
   
    #general pages
    path('', views.defaultHome, name='defaultHome'),
    path('courses', views.courses, name='courses'),
    path('info', views.info, name='info'),

    #login urls
    path('sign-up/', views.sign_up, name='sign_up'),
    path('home', views.home, name='home'),

    #Password reset URLs
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="reset_password.html"), 
         name="reset_password"),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_msg.html"), 
         name="password_reset_done"), #Deals with notifying the user that the email was sent

    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="new_password.html"), 
         name="password_reset_confirm"), # deals with from to reset pwd

    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"), 
         name="password_reset_complete"),

    #APPOINTMENT URLS
    path('appointment_insert', views.appointment_form, name='appointment_insert'),

    path('appointment_list', views.appointment_list, name='appointment_list'),

    path('appointment_insert/<int:id>', views.appointment_form, name='appointment_update'),

    path('appointment_insert/delete/<int:id>/', views.appointment_delete, name='appointment_delete'),

    #Student Appointment URLs
    path('stu_appointment_list', views.stu_appointment_list, name='stu_appointment_list'),

    #Staff Appointment URLs
    path('staff_appointment_list', views.staff_appointment_list, name='staff_appointment_list'),
  

]