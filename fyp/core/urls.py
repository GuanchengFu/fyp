from django.urls import path
from core import views


app_name = 'core'

urlpatterns = [
	path('', views.index, name='index'),
	path('about/', views.about, name='about'),
	path('register/', views.register, name='register'),
	path('redirected/', views.redirected, name='redirected'),
	path('professorregister/', views.professor_register, name='proRegister'),
	path('candidateregister/', views.candidate_register, name='canRegister'),
	path('logout/', views.user_logout, name='logout'),
	path('dashboard/', views.show_dashboard, name='dashboard'),
	path('dashboard/uploadfile/', views.upload_file, name='uploadfile'),
	path('dashboard/file/<int:file_id>', views.edit_file, name='edit_file'),
	path('dashboard/file/<int:file_id>/sendMessage', views.dispose_message_form, name='send_message'),
	path('dashboard/file/<int:file_id>/delete', views.delete_file, name='delete_file'),
	path('dashboard/messages', views.show_message, name='show_message'),
	path('dashboard/messages/compose', views.send_message, name='send_message'),
	path('dashboard/messages/outbox', views.outbox, name='outbox'),
	path('dashboard/messages/trash', views.trash, name='trash_box'),
	path('dashboard/connection', views.connection, name='connection'),
]