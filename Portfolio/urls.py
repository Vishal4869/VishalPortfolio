
from django.contrib import admin
from django.urls import path,include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',Home,name='index'),
    path('captcha/',include("captcha.urls"))
# ]+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

