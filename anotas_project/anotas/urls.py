from django.urls import path
from anotas import views
app_name = 'anotas'
from anotas import views
app_name = 'anotas'
urlpatterns = [
path('', views.home, name='home'),
path('about/', views.about, name='about'),
path('subject/<slug:subject_name_slug>/',views.show_subject, name='show_subject'),
path('add_category/', views.add_category, name='add_category'),
path('add_subject/', views.add_subject, name='add_subject'),
path('register/', views.register, name='register'),
path('login/', views.user_login, name='login'),
path('restricted/', views.restricted, name='restricted'),
path('logout/', views.user_logout, name='logout'),
path('user/note/', views.add_note, name='note reader'),
path('user/', views.user_page, name='user page'),
path('user/<slug:note_name_slug>/',views.note_editor, name='note_editor'),
]