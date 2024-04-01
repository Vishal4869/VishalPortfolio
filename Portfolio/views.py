from django.shortcuts import render,redirect

from .models import *
from .forms import ContactForm, MyForm
# Create your views here.

def Home(request):

    projects=Project.objects.all().order_by('srno')
    cert=Certifications.objects.all().order_by('srno')

    resume=Resume.objects.first()

    if request.method=="POST":
      form=MyForm(request.POST)
      
      if form.is_valid():
        contact_form=ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()

        print("success")
      else:
        print("fail")
         

    form=MyForm()
    contact_form=ContactForm(use_required_attribute=False)

    context={'resume':resume,'projects':projects,'cert':cert,"form":form,'contact_form':contact_form}

    return render(request,'index.html',context)

