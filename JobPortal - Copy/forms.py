from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



class StylishForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class CandidateForm(StylishForm):
	class Meta:
		model = Candidates
		fields = '__all__'
		exclude = ['user']

class CompanyForm(StylishForm):
	class Meta:
		model = Company
		fields = '__all__'
		exclude = ['user']		
	

class ApplyForm(ModelForm):
    class Meta:
        model=Candidates
        fields="__all__"


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']


class CreateJobForm(StylishForm):
	class Meta:
		model = Jobcreate
		fields = '__all__'
		exclude=['company_name']
		
        
		