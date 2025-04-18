from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/files/delete/<int:file_id>/', views.delete_file, name='delete_file'),
] 