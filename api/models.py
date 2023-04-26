from django.db import models
import bcrypt
import random
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


gauth = GoogleAuth()
drive = GoogleDrive(gauth)

folder = '1iwZ2iE3e_7tfegKAI-halhhK9fn9Nv-A'

student = "student"
teacher = "teacher"
admin = "admin"

USER_CHOICES = (
    (student, "student"),
    (teacher, "teacher"),
    (admin, "admin")
)

def name_image(instance,filename):
    name = instance.name
    email = instance.email
    arr1 = email.split("@")
    arr = name.split()
    name = "".join(arr)
    name = name.lower()
    return arr1[0].lower() + '.jpg'

def name_profile_image(instance,filename):
    name = instance.name
    email = instance.email
    arr1 = email.split("@")
    email = arr1[0].lower()
    return email + 'profile' + '.jpg'

def generatepass():
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"

    string = lower + upper + numbers
    password = "".join(random.sample(string, 7))
    return password

class student_models(models.Model):

    name=models.CharField(max_length=20,default='None',blank=True)
    roll_no = models.CharField(max_length=20,unique=True,default='None')
    email=models.CharField(max_length=50,unique=True,default='None')
    password=models.CharField(max_length=20,default=generatepass())
    user_type = models.CharField(max_length=10,choices=USER_CHOICES,default=student)
    fathers_name=models.CharField(max_length=20,default='',blank=True)
    mothers_name=models.CharField(max_length=20,default='',blank=True)
    date_of_birth=models.DateField(auto_now_add=True)
    gender=models.CharField(max_length=10,default='')
    session=models.CharField(max_length=10,default='')
    college_Name=models.CharField(max_length=100,default='')
    course_name=models.CharField(max_length=50,default='')
    branch=models.CharField(max_length=100,default='')
    semester=models.CharField(max_length=20,default='',blank=True)
    year=models.CharField(max_length=20,default='',blank=True)
    phone_number=models.CharField(max_length=20,default='',blank=True)
    address=models.CharField(max_length=300,default='',blank=True)   
    city=models.CharField(max_length=50,default='',blank=True)
    state=models.CharField(max_length=50,default='',blank=True)
    country=models.CharField(max_length=50,default='',blank=True)
    status=models.BooleanField(default=False)
    skills = models.JSONField(default=dict)
    social_links = models.JSONField(default=dict)
    profile_image = models.ImageField(upload_to=name_profile_image, blank=True)
    image = models.ImageField(upload_to=name_image, blank=True)
    description = models.CharField(max_length=200,default='',blank=True)


    # def save(self, *args, **kwargs):
    #     password = self.password
    #     bytes = password.encode('utf-8')
    #     salt = bcrypt.gensalt()
    #     hash = bcrypt.hashpw(bytes,salt)   
    #     self.password = hash
    #     print(self.password)
    #     super(ImageModel, self).save()


class teacher_models(models.Model):

    name=models.CharField(max_length=20,default='None',blank=True)
    email=models.CharField(max_length=50,unique=True,default='None')
    password=models.CharField(max_length=20,default=generatepass())
    user_type = models.CharField(max_length=10,choices=USER_CHOICES,default=teacher)
    date_of_birth=models.DateField(auto_now_add=True)
    gender=models.CharField(max_length=10,default='')
    college_Name=models.CharField(max_length=100,default='')
    course_name=models.CharField(max_length=50,default='')
    branch=models.CharField(max_length=100,default='')
    phone_number=models.CharField(max_length=20,default='',blank=True)
    address=models.CharField(max_length=300,default='',blank=True) 
    city=models.CharField(max_length=50,default='',blank=True)
    state=models.CharField(max_length=50,default='',blank=True)
    country=models.CharField(max_length=50,default='',blank=True)
    status=models.BooleanField(default=False)
    specialized_in = models.JSONField(default=dict)
    social_links = models.JSONField(default=dict)
    subjects = models.JSONField(default=dict)
    profile_image = models.ImageField(upload_to=name_profile_image, blank=True)
    image = models.ImageField(upload_to=name_image, blank=True)
    designation = models.CharField(max_length=20,default='',blank=True)
    description = models.CharField(max_length=200,default='',blank=True)
