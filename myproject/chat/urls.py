from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('send/', views.send_message, name='send_message'),
    path('get_suggestions/', views.get_suggestions, name='get_suggestions'),
    path('settings/', views.settings_dashboard, name='settings_dashboard'),
    path('settings/delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('test/', views.test_view, name='test_view'),
    path('test_send/', views.test_send, name='test_send'),
    path('status/', lambda request: views.JsonResponse({'status': 'ok'}), name='status'),
    path('update_model_params/', views.update_model_params, name='update_model_params'),
    path('get_site_name/', views.get_site_name, name='get_site_name'),
    path('notify_prompt_update/', views.notify_prompt_update, name='notify_prompt_update'),
] 