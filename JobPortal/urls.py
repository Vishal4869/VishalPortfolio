from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',main,name='main'),
    path('alljobs',allJobs,name='alljobs'),
    path('rlogin/',recruiterLogin,name='rlogin'),
    path('clogin/',candidateLogin,name='clogin'),
    path('logout/',logoutUser,name='logout'),
    path('register/', registerPage, name="register"),
    path('apply/<uuid:aid>',applyPage,name='apply'),
    path('invite/<int:iid>',invitePage,name='invite'),
    path('contact/', contact,name='contact'),
    path('faq/', FAQ,name='faq'),
    path('hworks/', Hworks,name='hworks'),
    path('aboutUs/', aboutUS,name='aboutUS'),
    path('jobView/<uuid:jid>', jobView,name='jobView'),
    path('search/', search,name='search'),
    path('csearch', csearch,name='csearch'),
    path('showvideo/<int:myid>', showvideo,name='showvideo'),
    path('candidate/', candidatePage, name="candidatePage"),
    path('recruiter/', recruiterPage, name="recruiterPage"),
    path('caccount/', caccountSettings, name="caccount"),
    path('raccount/', raccountSettings, name="raccount"),
    path('jobcreate/', jobCreate, name="jobcreate"),
    path('jobdelete/<int:pid>', jobDelete, name="jobdelete"),
    path('jobedit/<int:eid>', jobEdit, name="jobedit"),
    path("change_password/",change_password,name="change_password"),
    path('all_category/', all_category, name='allcategory'),
    path('job_category/<str:cat>/', job_category, name='jobcategory')

    
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)