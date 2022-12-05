from contextlib import nullcontext
from email.policy import default
from django.db import models
from _auth.models import CustomUser, RadiologistProfile


# Create your models here.
 
# class Radiologist(models.Model):
#     name = models.CharField(max_length=100)
#     id = models.AutoField(primary_key=True)
#     mobile_number = models.CharField(max_length=10, unique=True)
#     national_id = models.CharField(max_length=10, unique=True)
#     password = models.CharField(max_length=100, default="123456")
#     user = models.OneToOneField(CustomUser, related_name= "profile", on_delete=models.CASCADE)
    
#     def __str__(self):
#         return self.name
    


class Patient(models.Model):
    name = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)
    mobile_number = models.CharField(max_length=11)
    radiologist = models.ForeignKey(RadiologistProfile, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)
    


class Scan(models.Model):
    
    input_image = models.ImageField(upload_to='images/input/', blank=True, null=True, unique=False)
    # output_image = models.ImageField(upload_to='images/output/', blank=True, null=True)
    output_image = models.CharField(max_length=1000, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True)
    patient =  models.ForeignKey(Patient, on_delete=models.CASCADE)
    labels = models.CharField(max_length=10000, blank=True, null=True)

