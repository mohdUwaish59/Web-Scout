from django.contrib import admin
from django.urls import path, include
from WebScoutApp import views
from django.conf import settings
from django.conf.urls.static import static

app_name='home'

urlpatterns = [
    #path('contact', views.contact, name='contact'),
    path('', views.home, name='home'),
    path('scrape', views.scrape, name='scrape'),
    
    #path('about', views.about, name='about'),
]