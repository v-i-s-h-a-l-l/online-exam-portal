from django.db import models

class LoginStudent(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=255)  # Store hashed passwords in production
    emailid=models.CharField(max_length=100,unique=True)
    otp=models.CharField(max_length=6,blank=True,null=True)
    dept=models.CharField(max_length=6)
    year=models.IntegerField()

class TeacherAdmin(models.Model):
    staffid=models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)  
    password = models.CharField(max_length=255)  # Store hashed passwords for security
    usertype = models.CharField(max_length=10, choices=[('teacher', 'Teacher'), ('admin', 'Admin')])
    emailid = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True) 
    dept=models.CharField(max_length=6) # Allow NULL values