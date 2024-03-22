from django.urls import path
from anotas import views
app_name = 'anotas'
from anotas import views
app_name = 'anotas'
urlpatterns = [
path('', views.home, name='home'),
path('about/', views.about, name='about'),
path('subject/<slug:subject_name_slug>/',views.show_subject, name='show_subject'),
path('subject/<slug:subject_name_slug>/add_note/', views.add_note, name='add_note'),
path('register/', views.register, name='register'),
path('login/', views.user_login, name='login'),
path('restricted/', views.restricted, name='restricted'),
path('logout/', views.user_logout, name='logout')
]