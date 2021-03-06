from django.urls import path
from core import views


app_name = 'core'

urlpatterns = [
	path('', views.index, name='index'),
	path('about/', views.AboutView.as_view(), name='about'),
	path('register/', views.register, name='register'),
	path('redirected/', views.redirected, name='redirected'),
	path('redirected/notifications/<int:notification_id>', views.view_message_from_notification, name='noti_redirect'),
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
	path('dashboard/connection/createGroup', views.create_group, name='create_group'),
	path('view/<int:message_id>', views.view_message, name='view_message'),
	path('view/redirected/<int:message_id>/', views.save_file, name='save_file_in_message'),
	path('dashboard/notifications/unread', views.notifications_unread, name='view_notifications'),
	path('dashboard/notifications/all',views.notifications_all, name='all_notifications'),
	path('dashboard/notifications/mark-all-as-read', views.mark_all_as_read, name='mark_all_as_read'),
	path('dashboard/notifications/delete-all', views.delete_all_read_notifications, name='delete_all_read_notifications'),
	path('dashboard/connection/add', views.AddNewRelationship.as_view(), name='add_new_relationship'),
]