from django.urls import path
from core import views


app_name = 'core'

urlpatterns = [
	path('', views.index, name='index'),
	path('about/', views.about, name='about'),
	#path('register/', views.register, name='register'),
	path('redirect/', views.redirect, name='redirect'),
	path('professorregister/', views.professorRegister, name='proRegister'),
	path('candidateregister/', views.candidateRegister, name='canRegister'),
	path('logout/', views.logout, name='logout'),
]