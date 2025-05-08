from django.urls import path
from . import views
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('send/', views.send_message, name='send_message'),
    path('admin/dashboard/', staff_member_required(views.admin_dashboard), name='admin_dashboard'),
    path('admin/delete/<int:file_id>/', staff_member_required(views.delete_file), name='delete_file'),
] 