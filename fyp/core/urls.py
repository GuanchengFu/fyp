from django.urls import path
from core import views


app_name = 'core'

urlpatterns = [
	path('', views.index, name='index'),
	path('about/', views.about, name='about'),
	path('register/', views.register, name='register'),
	path('redirected/', views.redirected, name='redirected'),
	path('professorregister/', views.professorRegister, name='proRegister'),
	path('candidateregister/', views.candidateRegister, name='canRegister'),
	path('logout/', views.user_logout, name='logout'),
	path('dashboard/', views.show_dashboard, name='dashboard'),
	path('dashboard/uploadfile/', views.upload_file, name='uploadfile'),
]