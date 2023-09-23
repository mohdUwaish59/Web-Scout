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
    #path('report', views.report, name='report'),
    path('report/<str:collection_name>/', views.report, name='report'),
    path('export_pdf/', views.export_pdf, name='export_pdf'),
    path('list_db', views.list_db, name='list_db'),
    
    #path('about', views.about, name='about'),
]