from contextlib import ContextDecorator
from django import forms
from captcha.fields import CaptchaField
from django.core.exceptions import ValidationError

from Portfolio.models import Contact

class StylishForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class ContactForm(StylishForm):
	class Meta:
		model = Contact
		fields = '__all__'
		


class MyForm(forms.Form):
    captcha=CaptchaField()

   
    # def clean_password(self):
    #     if self.data['password'] != self.data['password_confirm']:
    #         raise forms.ValidationError('Passwords are not the same')
    #     return self.data['password']