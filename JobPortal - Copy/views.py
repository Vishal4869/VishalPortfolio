from collections import namedtuple
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth import login,logout,authenticate
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import apply_user, unauthenticated_user, allowed_users, admin_only,home_page
from django.contrib.auth.models import Group
from functools import reduce


# Create your views here.

# Main page 

@home_page
def main(request):
    companies=Jobcreate.objects.all().order_by('min_experience')
    li=[]
    context = {
    'companies': companies,'li':li
    }
    return render(request,'main.html',context)

def allJobs(request):
    companies=Jobcreate.objects.all().order_by('-date')
    li=[]


    if request.user.is_authenticated:
        jb=ApplyJob.objects.filter(user=request.user)
    
        for i in jb:
            ii=i.job_id.id
            li.append(ii)
            
    context = {
    'companies': companies,'li':li
    }
    return render(request,'allJobs.html',context)


def search(request):
    
    li=[]

    if request.user.is_authenticated:
        jb=ApplyJob.objects.filter(user=request.user)
    
        for i in jb:
            ii=i.job_id.id
            li.append(ii)
       
    squery= request.GET.get('search1')
    
    lquery= request.GET.get('search2')

    if(squery == '' ):
        squery=0
    
    if(lquery == '') :
        lquery=0
    
    companies =searchMatch(lquery,squery)
   
    
    context={
        'companies':companies,
        'msg' : '',
        'li':li
    }
    if len(companies)==0 :
        context={'msg':"Please  enter relevant search query"}  
    return render(request,'allJobs.html',context)

def searchMatch(lquery,squery):
    
    companies=Jobcreate.objects.filter(company_name__company_name__icontains=squery) or Jobcreate.objects.filter(skills__icontains=squery) or Jobcreate.objects.filter(job_position__icontains=squery)  or Jobcreate.objects.filter(Location__icontains=lquery) 
    return companies


def searchMatch2(lquery,squery, item):
    
    if (item.skills or item.job_position)is not None:
    
        if (squery.upper() in squery.upper() in item.job_position.upper() or item.skills) and lquery.upper() in item.Location.upper():
            return True
        else:
            return False


def csearch(request):

    recruiter2=request.user.company
    cquery= request.GET.get('search1')
    

    if(cquery == '' ):
        cquery=0
    
    candidates=Candidates.objects.filter(skills__icontains=cquery) or Candidates.objects.filter(applicant_name__icontains=cquery)
   
    alljobs=Jobcreate.objects.all()
    usrjobs=alljobs.filter(company_name=recruiter2)

    inv=Invite.objects.filter(company_name=recruiter2)
   
    context={
        'cancard':candidates, 'msg' : '','li2':inv,'usrjobs':usrjobs
    }
    
    if len(candidates)==0 :
        context={'msg':"Please  enter relevant search query"}  
    return render(request,'rsearch.html',context)


def logoutUser(request):
    logout(request)
    return redirect('main')


@login_required(login_url='clogin')
@allowed_users(allowed_roles=['jobseeker'])
@apply_user
def applyPage(request,aid):
    user = request.user
    candidates3=request.user.candidates
    applycompany = Jobcreate.objects.get(id=aid)
    companyname=applycompany.company_name
    job_position=applycompany.job_position
    ApplyJob.objects.create(user=user,company_name=companyname,job_id=applycompany,job_position=job_position)
    return redirect('candidatePage')
    
@login_required(login_url='rlogin')
@allowed_users(allowed_roles=['Hr'])
def invitePage(request,iid):
    squery= request.POST.get('cars')
    user = request.user
    company_name=user.company
    applicant_name=Candidates.objects.get(id=iid)
    company = Jobcreate.objects.get(id=squery)
    job_position=company.job_position
    Invite.objects.create(user=user,applicant_name=applicant_name,company_name=company_name,job_id=company, job_position= job_position)
    return redirect('recruiterPage')
    

def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'contact.html', {'thank': thank})

def FAQ(request):
    return render(request, 'faq.html')

def Hworks(request):
    return render(request, 'hworks.html')


def jobView(request,jid):

    li=[]
    
    company = Jobcreate.objects.filter(id=jid)

    if request.user.is_authenticated:
        jb=ApplyJob.objects.filter(user=request.user)


        for i in jb:
            ii=i.job_id.id
            li.append(ii)

    

    context = {'company':company[0],'jid':jid,'li':li}
    return render(request, 'jobView.html', context)
    
def aboutUS(request):

    return render(request, 'aboutUS.html')


@allowed_users(allowed_roles=['jobseeker','Hr','Admins'])
def showvideo(request,myid):

    videofile=Candidates.objects.filter(id=myid)
   
    return render(request, 'videoplayer.html',{'videofile':videofile[0]} )


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                group1=request.POST['grp']
                usern = form.cleaned_data.get('username')
                uid = User.objects.get(username=usern)
                
                if group1 == 'recruiter':
                    my_group = Group.objects.get(name='Hr') 
                    uid.groups.add(my_group)
                    Company.objects.create(user=uid)
                    
                else :
                    my_group = Group.objects.get(name='jobseeker') 
                    uid.groups.add(my_group)
                    Candidates.objects.create(user=uid)
                
                messages.success(request, 'Account was created for ' + usern)

                return redirect('clogin')
            

        context = {'form':form}
        return render(request, 'register.html', context)


def candidateLogin(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('candidatePage')
            else:
                messages.info(request, 'Username OR Password is incorrect')

        context = {}
        return render(request, 'clogin.html', context)

def recruiterLogin(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
       if request.method=="POST":
        name=request.POST.get('username')
        pwd=request.POST.get('password')

        user=authenticate(request,username=name,password=pwd)

        if user is not None:
                login(request,user)
                return redirect('recruiterPage')
        else:
            messages.info(request, 'Username OR Password is incorrect')

    context = {}
    return render(request, 'rlogin.html', context)

@login_required(login_url='clogin')
@allowed_users(allowed_roles=['jobseeker'])
def candidatePage(request):

    candidates1 = request.user
    can2=Candidates.objects.get(user=candidates1)
    can3=can2.skills
    can4=''
    if can3 is not None:
        can4=can3.split(',')
    form = CandidateForm(instance=candidates1.candidates)
    allcompanies=Jobcreate.objects.all()
   
    appliedjobs=Invite.objects.filter(applicant_name=candidates1.candidates)
    totaply=appliedjobs.count()

    tinv=[]
    
    for i in appliedjobs:
        d2=i.job_id.id
        y=Jobcreate.objects.get(id=d2)
        tinv.append(y)


    lquery= ''
    
    companies2=[]
    
    for squery in can4:
        companies=[item for item in allcompanies if searchMatch2(lquery,squery, item)]
        companies2.append(companies)
    
    try :
        single_list = reduce(lambda x,y: x+y, companies2)
    except:
        single_list =[]  
    single_list2=set(single_list)

    jb=ApplyJob.objects.filter(user=candidates1)
    li=[]
    jb3=[]


    for i in jb:
        ii=i.job_id.id
        li.append(ii)
        jb2=Jobcreate.objects.get(id=ii)
        jb3.append(jb2)
        
    
    tot_li=len(li)
        
    
    context = {'companies': single_list2,'c':can2 ,'li':li,'tot_li':tot_li,'applied':jb3,'form':form,'totaply':totaply,
    'tinv':tinv}
    return render(request, 'candidate.html', context)


@login_required(login_url='rlogin')
@allowed_users(allowed_roles=['Hr'])
def recruiterPage(request):
    recruiter2 = request.user.company
    alljobs=Jobcreate.objects.all()
    usrjobs=alljobs.filter(company_name=recruiter2)
    usrjobstotal=usrjobs.count()
   
    
    appliedjob=ApplyJob.objects.filter(company_name=recruiter2)
    
    appusr=[]
    upos=[]
    for a in appliedjob:   
        d1=a.user
        s1=a.job_position
        x=Candidates.objects.get(user=d1)
        appusr.append(x)
        upos.append(s1)  

    cancard=set(appusr)

    totalappusr=len(appusr)

    inv=Invite.objects.filter(company_name=recruiter2)

    context = {'candidates':appusr,'alljobs':alljobs,'usrjobs':usrjobs,'usrjobstotal':usrjobstotal,'totalappusr':totalappusr,
    'bar_data': zip(upos, appusr),'cancard':cancard,'li2':inv}
    return render(request, 'recruiter.html', context)

@allowed_users(allowed_roles=['Hr'])
def raccountSettings(request):
    company = request.user.company
    form = CompanyForm(instance=company)

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES,instance=company)
        if form.is_valid():
            form.save()


    context = {'form':form}
    return render(request, 'raccount.html', context)

@allowed_users(allowed_roles=['jobseeker'])
def caccountSettings(request):
    candidates = request.user.candidates
    form = CandidateForm(instance=candidates)

    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES,instance=candidates)
        if form.is_valid():
            form.save()


    context = {'form':form}
    return render(request, 'caccount.html', context)

@allowed_users(allowed_roles=['Hr','Admins'])
def jobCreate(request):

    error=''
    jobcreate1 = request.user.company
    alljobs=Jobcreate.objects.all()
    usrjobs=alljobs.filter(company_name=jobcreate1)
    usrjobstotal=usrjobs.count()

    form = CreateJobForm(instance=jobcreate1)
    msg=''
    if request.method == 'POST':
        form = CreateJobForm(request.POST,instance=jobcreate1)
        
        if form.is_valid():

            job_position=request.POST['job_position']
            job_description=request.POST['job_description']
            min_salary=request.POST['min_salary']
            max_salary=request.POST['max_salary']
            min_experience=request.POST['min_experience']
            max_experience=request.POST['max_experience']
            Location=request.POST['Location']

            Jobcreate.objects.create(company_name=jobcreate1,job_position=job_position,job_description=job_description,min_salary=min_salary,
            max_salary=max_salary,min_experience=min_experience,max_experience=max_experience,Location=Location)

            msg='jobcreated'

            
   
    context = {'form':form, 'error':error,'usrjobs':usrjobs,'usrjobstotal':usrjobstotal,'msg':msg}
    return render(request, 'jobcreate.html', context)

@allowed_users(allowed_roles=['Hr','Admins'])
def jobDelete(request,pid):
    jobdelete=Jobcreate.objects.get(id=pid)
    jobdelete.delete()
    return redirect('recruiterPage')

@allowed_users(allowed_roles=['Hr','Admins'])
def jobEdit(request,eid):
    editjob=Jobcreate.objects.get(id=eid)
    form = CreateJobForm(instance=editjob)
    if request.method == 'POST':
        form = CreateJobForm(request.POST, request.FILES,instance=editjob)
        if form.is_valid():
            form.save()
        return redirect('recruiterPage')


    context = {'form':form,'eid':eid}
    return render(request, 'editjob.html', context)

@login_required(login_url='clogin')
def change_password(request):
    context={}
    
    if request.method=="POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]
        
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check==True:
            user.set_password(new_pas)
            user.save()
            context["msz"] = "Password Changed Successfully!!!"
            context["col"] = "alert-success"
            user = User.objects.get(username=un)
            login(request,user)
        else:
            context["msz"] = "Incorrect Current Password"
            context["col"] = "alert-danger"

    return render(request,"change_password.html",context)

def jobs_per_category(cat):
    jobs = Jobcreate.objects.filter(job_category=cat)
    return len(jobs)


def all_category(request):
    context = {
    'cat': [[i[0], jobs_per_category(i[0])] for i in CATEGORY],
    }
    return render(request,"allCategory.html",context)

def job_category(request, cat):
    companies = Jobcreate.objects.filter(job_category=cat).order_by('-date')
    li=[]


    if request.user.is_authenticated:
        jb=ApplyJob.objects.filter(user=request.user)
    
        for i in jb:
            ii=i.job_id.id
            li.append(ii)
            
    context = {
    'companies': companies,'li':li, 'cat':cat,
    }
    return render(request, 'jobCategory.html', context)
