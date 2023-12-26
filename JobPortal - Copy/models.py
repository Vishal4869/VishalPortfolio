from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres import *
from datetime import datetime
import uuid


CATEGORY = (
    ('Accounting and Consulting', 'Accounting and Consulting'),
    ('Admin Support', 'Admin Support'),
    ('Customer Service', 'Customer Service'),
    ('Data Science and Analysis', 'Data Science and Analysis'),
    ('Design and Creative', 'Design and Creative'),
    ('Engineering and Architecture', 'Engineering and Architecture'),
    ('IT and Networking', 'IT and Networking'),
    ('Legal', 'Legal'),
    ('Sales and Marketing', 'Sales and Marketing'),
    ('Translation', 'Translation'),
    ('Web, Mobile, and Software Development', 'Web, Mobile, and Software Development'),
    ('Writing', 'Writing'),
    ('Others', 'Others'),
    )


# Create your models here.
class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    company_name=models.CharField(max_length=200,null=True,unique=True)
    company_logo = models.ImageField(default="profile2.png", null=True, blank=True)
    def __str__(self):
        return self.company_name


class Jobcreate(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name= models.ForeignKey(Company, null=True, on_delete= models.SET_NULL)
    job_position=models.CharField(max_length=200,null=True)
    skills=models.CharField(max_length=300,null=True)
    disability=models.CharField(max_length=100,null=True)
    job_description=models.TextField(max_length=3000,null=True)
    min_salary=models.IntegerField(null=True)
    max_salary=models.IntegerField(null=True)
    min_experience=models.IntegerField(null=True)
    max_experience=models.IntegerField(null=True)
    Location=models.CharField(max_length=2000,null=True)
    date = models.DateTimeField(default=datetime.today(), blank=True)
    job_category = models.CharField(max_length=200, choices=CATEGORY, default='Others')


    def __str__(self):
        return f'{self.company_name} {self.job_position}'
    


class Candidates(models.Model):
    category=(
        ('Male','male'),
        ('Female','female'),
        ('Other','other'),
    )
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    applicant_name=models.CharField(max_length=200,null=True)
    education=models.CharField(max_length=200,null=True, blank=True)
    address= models.CharField(max_length=300,null=True, blank=True)
    skills=models.CharField(max_length=300,null=True)
    applicant_dob=models.DateField(null=True, blank=True)
    gender= models.CharField(max_length=200,null=True,choices=category, blank=True)
    contact_no= models.CharField(max_length=200,null=True, blank=True)
    email= models.CharField(max_length=200,null=True, blank=True)
    year_experience=models.IntegerField(null=True, blank=True)
    month_experience=models.IntegerField(null=True, blank=True)
    previous_work=models.TextField(max_length=3000,null=True, blank=True)
    intro=models.FileField(null=True, blank=True)
    aadhar_card=models.FileField(default="profile1.png", null=True, blank=True)
    pancard=models.FileField(default="profile1.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    disability_certificate=models.FileField(default="profile1.png", null=True, blank=True)
    certifications=models.FileField(default="profile1.png", null=True, blank=True)
    

    def __str__(self):
        return self.applicant_name

class ApplyJob(models.Model):

    company_name= models.ForeignKey(Company, null=True, on_delete= models.SET_NULL)
    job_id= models.ForeignKey(Jobcreate, null=True, on_delete= models.SET_NULL)
    job_position=models.CharField(max_length=200,null=True)
    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    application_date=models.DateTimeField(default=datetime.today(), blank=True)

    def __str__(self):
        return f'{self.user} {self.company_name}'

class Invite(models.Model):

    company_name= models.ForeignKey(Company, null=True, on_delete= models.SET_NULL)
    job_id= models.ForeignKey(Jobcreate, null=True, on_delete= models.SET_NULL)
    job_position=models.CharField(max_length=200,null=True)
    applicant_name= models.ForeignKey(Candidates, null=True, on_delete= models.SET_NULL)
    user=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    invite_date=models.DateTimeField(default=datetime.today(), blank=True)

    def __str__(self):
        return f'{self.user} {self.applicant_name}'



class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=100, default="")
    desc = models.TextField(max_length=500, default="")


    def __str__(self):
        return self.name

        