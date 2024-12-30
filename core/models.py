from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import os
from django.utils import timezone

# Create your models here.
def file_path(request,filename):
    oldfilename = filename
    timenow = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    filename = "%s%s"%(timenow,oldfilename)
    return os.path.join("uploads/",filename)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    ROLE_CHOICES = (
        (0,'Admin'),
        (1,'Theater'),
        (2,'User')
    )
    usertype = models.IntegerField(choices=ROLE_CHOICES,null=True)    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    
class Theatre(models.Model):
    theatrename = models.CharField(max_length=255)
    theatrelocation = models.TextField()
    theatredescription = models.TextField()
    rating = models.CharField(max_length=255)
    userid = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)

 
class MovieShow(models.Model):
    theatreid = models.ForeignKey(Theatre, null=True, on_delete=models.CASCADE)
    moviename = models.CharField(max_length=255)
    moviedescription = models.TextField()
    movielanguage = models.CharField(max_length=255,default=True)
    moviegenere = models.CharField(max_length=255)
    sensorrate = models.CharField(max_length=255)
    image = models.ImageField(upload_to=file_path,null = True, blank = True)
   
        
class RegistrationTable(models.Model):
    username = models.CharField(max_length=255)
    useraddress = models.TextField()
    userid = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    

class BookingTable(models.Model):
    booking_time = models.DateTimeField()
    ROLE_CHOICES = (
        (0,'In Progress'),
        (1,'Approved'),
        (2,'Cancelled')
    )
    current_time= models.DateTimeField(default=timezone.localtime)
    status = models.IntegerField(choices=ROLE_CHOICES, null=True)
    userid = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    movieid = models.ForeignKey(MovieShow, null=True, on_delete=models.CASCADE)
    theatreid = models.ForeignKey(Theatre, null=True, on_delete=models.CASCADE)
    
class ReviewTable(models.Model):
    userid = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    movieid = models.ForeignKey(MovieShow, null=True, on_delete=models.CASCADE)
    reviewdescription = models.TextField()
    reviewrating = models.CharField(max_length=255)